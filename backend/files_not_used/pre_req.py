# import html
# from bs4 import BeautifulSoup
# import requests
# from fastapi import APIRouter
# from pydantic import BaseModel



# # Create router
# router = APIRouter()

# class ExtractRequest(BaseModel):
#     major: str

# # Gets the pid for the program the user has selected in the form
# def get_course_pid(course: str):
#     endpoint = "https://uvic.kuali.co/api/v1/catalog/courses/67855445a0fe4e9a3f0baf82"

#     response = requests.get(endpoint)
#     if response.status_code == 200:
#         data_program_pid = response.json()
#         # print(data_program_pid)
#     for program in data_program_pid:
#         if program['__catalogCourseId'] ==course:
#             return program['pid']
#             print(program['title'], program["pid"])

# # Gets the course list for the major the user entered
# def get_course_data(course: str):

#     pid = get_course_pid(course)
#     print("pid: ", pid)
#     endpoint = f"https://uvic.kuali.co/api/v1/catalog/course/67855445a0fe4e9a3f0baf82/{pid}"

#     response = requests.get(endpoint)
#     if response.status_code==200:
#         data = response.json()
#         # print(data)

#     # getting raw encoded program courses 
#     raw_program_req = data["preAndCorequisites"]
#     # print(raw_program_req)

#     # Decode Unicode escapes (turns \u003C into <)
#     decoded_program = raw_program_req.encode().decode('unicode_escape')

#     # Unescape any HTML entities (like &lt; into <)
#     clean_html = html.unescape(decoded_program)

#     soup = BeautifulSoup(clean_html, 'html.parser')

#     prereq_blocks = []

#     for li in soup.find_all("li"):
#         # Check if this <li> contains a nested <ul> – i.e., a grouped rule
#         nested = li.find("ul")
#         if nested:
#             rule_type_text = li.get_text(separator=" ", strip=True).split(":")[0]
#             rule = {"type": rule_type_text, "courses": []}
#             for nested_li in nested.find_all("li"):
#                 course = nested_li.find("a")
#                 if course:
#                     rule["courses"].append(course.text.strip())
#             prereq_blocks.append(rule)
#     print(prereq_blocks)


# # # main API
# # @router.post("/extract_courses")
# # def extracted_courses(req:ExtractRequest):

# #     try:
# #         return get_major_data(req.major)
# #         # print()
# #     except Exception as e:
# #         return {"error": str(e)}




# if __name__ == "__main__":
#     get_course_data("SENG426")