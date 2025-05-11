import re
import requests


courses_completed = requests.get("http://127.0.0.1:8000/courses_completed").text
completed_courses_list =  [c.strip() for c in courses_completed.split(",")]
# print("hello course compl: ", courses_completed)

course_list = requests.get("http://127.0.0.1:8000/course_list").text
course_list_l = [c.strip() for c in course_list.split(",")]
# print("hello course list: ", lt1)

course_not_comp = []
for course in course_list_l:
    if course not in completed_courses_list:
        course_not_comp.append(course)

for course in course_not_comp:
    match = re.match(r"([A-Z]+)(\d+):", course)
    if match:
        subject = match.group(1)
        number = match.group(2)
        print(f"Subject: {subject}, Number: {number}")

# print(course_not_comp)