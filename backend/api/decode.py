import html
from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter
from pydantic import BaseModel



# Create router
router = APIRouter()

class ExtractRequest(BaseModel):
    major: str

# Gets the pid for the program the user has selected in the form
def get_program_pid(major: str):
    endpoint = "https://uvic.kuali.co/api/v1/catalog/programs/67855445a0fe4e9a3f0baf82"

    response = requests.get(endpoint)
    if response.status_code == 200:
        data_program_pid = response.json()
        # print(data_program_pid)
    for program in data_program_pid:
        if program['title'] ==major:
            return program['pid']
            # print(program['title'], program["pid"])

# Gets the course list for the major the user entered
def get_major_data(major: str):

    pid = get_program_pid(major)
    print("pid: ", pid)
    endpoint = f"https://uvic.kuali.co/api/v1/catalog/program/67855445a0fe4e9a3f0baf82/{pid}"

    response = requests.get(endpoint)
    if response.status_code==200:
        data = response.json()

    # getting raw encoded program courses 
    raw_program_req = data["programRequirements"]

    # Decode Unicode escapes (turns \u003C into <)
    decoded_program = raw_program_req.encode().decode('unicode_escape')

    # Unescape any HTML entities (like &lt; into <)
    clean_html = html.unescape(decoded_program)

    soup = BeautifulSoup(clean_html, 'html.parser')

    # storing all the program courses in this list
    course_list = []

    # Loop through all <li> tags
    for li in soup.find_all('li'):
        # Only process leaf <li> (no inner <ul>)
        if not li.find('ul'):
            a_tag = li.find('a')
            if a_tag and a_tag.text.strip():
                #  if Course with <a> tag
                course_code = a_tag.text.strip()
                full_text = li.get_text(" ").strip()

                # Clean up: remove course code from text
                if full_text.startswith(course_code):
                    rest_of_text = full_text[len(course_code):].strip(" -–:")
                else:
                    rest_of_text = full_text  # fallback

                course_list.append(course_code+": "+rest_of_text)

            else:
                # CASE 2️⃣: No <a> tag, it's a plain text elective
                elective_text = li.get_text(" ").strip()
                course_list.append(elective_text)

    # Remove duplicates while preserving order
    course_list = list(dict.fromkeys(course_list))
    print(course_list)
    return course_list
   


# main API
@router.post("/extract_courses")
def extracted_courses(req:ExtractRequest):

    try:
        return get_major_data(req.major)
        # print()
    except Exception as e:
        return {"error": str(e)}




# if __name__ == "__main__":
#     get_major_data("Computer Engineering")