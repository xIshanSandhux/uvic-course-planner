import requests


courses_completed = requests.get("http://127.0.0.1:8000/courses_completed")
list2 = list(courses_completed)
print("hello course compl: ", courses_completed.json())

course_list = requests.get("http://127.0.0.1:8000/course_list")
list1 = list(course_list)
print("hello course list: ", course_list.json())

# for i in range(len(courses_completed)):
