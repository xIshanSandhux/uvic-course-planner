# backend/api/decode.py
# Command to run this file: python -m backend.api.decode
import html
import json
from sqlalchemy import select
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio

from backend.db import database, majors
  # relative import from backend/db.py

router = APIRouter()

class ExtractRequest(BaseModel):
    major: str


# Helper Function to return the major pid
def get_program_pid(major: str) -> str:
    """Lookup the program pid for a given major title."""
    endpoint = "https://uvic.kuali.co/api/v1/catalog/programs/67855445a0fe4e9a3f0baf82"
    resp = requests.get(endpoint)
    if not resp.ok:
        raise HTTPException(status_code=502, detail="Failed to fetch program list")
    for program in resp.json():
        if program.get("title") == major:
            return program["pid"]
    raise HTTPException(status_code=404, detail=f"Program '{major}' not found")


# Helper function to decode + return course list
def parse_program_requirements(pid: str):
    """Fetch & decode the HTML program requirements into code/description pairs."""
    endpoint = f"https://uvic.kuali.co/api/v1/catalog/program/67855445a0fe4e9a3f0baf82/{pid}"
    resp = requests.get(endpoint)
    if not resp.ok:
        raise HTTPException(status_code=502, detail="Failed to fetch program requirements")
    raw_html = resp.json().get("programRequirements", "")
    # Decode escaped unicode + HTML entities
    decoded = raw_html.encode().decode("unicode_escape")
    clean    = html.unescape(decoded)
    soup     = BeautifulSoup(clean, "html.parser")

    courses = []
    for li in soup.find_all("li"):
        # only leaf items (no nested <ul>)
        if li.find("ul"):
            continue

        a_tag = li.find("a")
        if a_tag and a_tag.text.strip():
            code = a_tag.text.strip()
            full = li.get_text(" ").strip()
            # strip the code off the front of the text
            desc = full[len(code):].strip(" -–:") if full.startswith(code) else full
        else:
            # plain‐text elective or heading
            code = None
            desc = li.get_text(" ").strip()

        courses.append({"code": code, "description": desc})

    # dedupe while preserving order
    seen = set()
    out  = []
    for c in courses:
        key = (c["code"], c["description"])
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


# Storing Major + pid + course list in the DB
async def tryial(major: str):

    # Initating connection
    await database.connect()

    # Get Major PID
    pid = get_program_pid(major)

    # Get Major course list
    course_list = parse_program_requirements(pid)

    # Storing major name + pid + course list in the majors table
    await database.execute(
        """
        INSERT INTO majors
            (major, major_pid, courses)
        VALUES
            (:major, :pid, :courses)
        ON CONFLICT (major) DO UPDATE
            SET major_pid    = EXCLUDED.major_pid,
                courses = EXCLUDED.courses;
        """,
        {
            "major": major,
            "pid": pid,
            "courses": json.dumps(course_list),
        },
    )

    # Ending Connection
    await database.disconnect()



# Gets the pid for the program the user has selected in the form
def get_course_pid(course: str):
    endpoint = "https://uvic.kuali.co/api/v1/catalog/courses/67855445a0fe4e9a3f0baf82"

    response = requests.get(endpoint)
    if response.status_code == 200:
        data_program_pid = response.json()
        # print(data_program_pid)
    for program in data_program_pid:
        if program['__catalogCourseId'] ==course:
            return program['pid']
            print(program['title'], program["pid"])

# Gets the course list for the major the user entered
async def get_course_data(major: str):

    await database.connect()
    query = select(majors.c.courses).where(majors.c.major == major)
    course_list = await database.fetch_one(query)
    # print(course_list['courses'])

    for course in course_list['courses']:
    # print(course['code'])
        course_pid = get_course_pid(course['code'])
        endpoint = f"https://uvic.kuali.co/api/v1/catalog/course/67855445a0fe4e9a3f0baf82/{course_pid}"

        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()

            # Parse prerequisites if they exist
            prereq_blocks = []
            if "preAndCorequisites" in data:
                raw_program_req = data["preAndCorequisites"]

                # Decode Unicode escapes (turns \u003C into <)
                decoded_program = raw_program_req.encode().decode('unicode_escape')

                # Unescape any HTML entities (like &lt; into <)
                clean_html = html.unescape(decoded_program)

                soup = BeautifulSoup(clean_html, 'html.parser')

                for li in soup.find_all("li"):
                    # Check if this <li> contains a nested <ul> – i.e., a grouped rule
                    nested = li.find("ul")
                    if nested:
                        rule_type_text = li.get_text(separator=" ", strip=True).split(":")[0]
                        rule = {"type": rule_type_text, "courses": []}
                        for nested_li in nested.find_all("li"):
                            nested_course = nested_li.find("a")
                            if nested_course:
                                rule["courses"].append(nested_course.text.strip())
                        prereq_blocks.append(rule)

            # Parse course description
            raw_program_desc = data['description']
            decoded_desc = raw_program_desc.encode().decode('unicode_escape')
            clean_html_desc = html.unescape(decoded_desc)
            soup_desc = BeautifulSoup(clean_html_desc, 'html.parser')
            plain_text = soup_desc.get_text()

            # Insert into database
            await database.execute(
                """
                INSERT INTO courses_main
                    (pid, course_code, course_name, prerequisites, credits,course_description)
                VALUES
                    (:pid, :course_code, :course_name, :prerequisites, :credits,:course_description)
                ON CONFLICT (pid) DO UPDATE
                    SET course_name = EXCLUDED.course_name,
                        prerequisites = EXCLUDED.prerequisites,
                        credits = EXCLUDED.credits;
                """,
                {
                    "pid": course_pid,
                    "course_code": course['code'],
                    "course_name": course['description'],
                    "prerequisites": json.dumps(prereq_blocks),
                    "credits": None,
                    "course_description":plain_text
                },
            )

    await database.disconnect()


    # pid = get_course_pid(course)
    # print("pid: ", pid)
    # endpoint = f"https://uvic.kuali.co/api/v1/catalog/course/67855445a0fe4e9a3f0baf82/{pid}"




    # response = requests.get(endpoint)
    # if response.status_code==200:
    #     data = response.json()
    #     # print(data)

    # # getting raw encoded program courses 
    # raw_program_req = data["preAndCorequisites"]
    # # print(raw_program_req)

    # # Decode Unicode escapes (turns \u003C into <)
    # decoded_program = raw_program_req.encode().decode('unicode_escape')

    # # Unescape any HTML entities (like &lt; into <)
    # clean_html = html.unescape(decoded_program)

    # soup = BeautifulSoup(clean_html, 'html.parser')

    # prereq_blocks = []

    # for li in soup.find_all("li"):
    #     # Check if this <li> contains a nested <ul> – i.e., a grouped rule
    #     nested = li.find("ul")
    #     if nested:
    #         rule_type_text = li.get_text(separator=" ", strip=True).split(":")[0]
    #         rule = {"type": rule_type_text, "courses": []}
    #         for nested_li in nested.find_all("li"):
    #             course = nested_li.find("a")
    #             if course:
    #                 rule["courses"].append(course.text.strip())
    #         prereq_blocks.append(rule)
    # print(prereq_blocks)












# @router.post("/extract_courses")
# async def extracted_courses(req: ExtractRequest):
#     """Fetch, parse, upsert into DB, and return the inserted course codes."""
#     # 1) Find the program PID
#     pid = get_program_pid(req.major)

#     # 2) Parse HTML into structured list
#     course_list = parse_program_requirements(pid)

#     # 3) Upsert each into your `courses` table
#     upserted = []
#     for item in course_list:
#         code = item["code"] or ""
#         desc = item["description"]
#         raw  = json.dumps(item)  # JSON-stringify for the JSON column

#         await database.execute(
#             """
#             INSERT INTO majors
#               major, major_pid, courses)
#             VALUES
#               (:major, :pid, :courses)
#             ON CONFLICT (catalog_course_id) DO UPDATE
#               SET title    = EXCLUDED.title,
#                   raw_json = EXCLUDED.raw_json;
#             """,
#             {
#                 "cid":     code,
#                 "pid":     None,
#                 "title":   desc,
#                 "credits": 0,
#                 "major":   req.major,
#                 "raw":     raw,
#             },
#         )
#         upserted.append(code)
#         print(upserted)

#     return {"inserted_courses": upserted}



if __name__ == "__main__":
   
    asyncio.run(get_course_data("Software Engineering"))