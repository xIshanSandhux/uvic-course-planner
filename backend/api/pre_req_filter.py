from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
import json
import re
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import select, update

from backend.db import database, courses_main,majors
  # relative import from backend/db.py

# Create router
router = APIRouter()

async def pre_req_fetch(course: str):
    await database.connect()
    match = re.search(r"\b[A-Z]{3,4}\d{3}\b", course)
    pre_reqs=[]
    if match:
        query = select(courses_main).where(courses_main.c.course_code == match.group(0))
        course_db = await database.fetch_one(query)
        pre_reqs = course_db['prerequisites']
        print(pre_reqs)
    await database.disconnect()
    return pre_reqs

async def pre_req_check():
    # courses = ['CSC115: Fundamentals of Programming II   (1.5)', 'MATH109: Introduction to Calculus   (1.5)', 'CHEM150: Engineering Chemistry   (1.5)', 'CSC230: Introduction to Computer Architecture   (1.5)', 'CSC225: Algorithms and Data Structures I   (1.5)', 'ECE260: Continuous-Time Signals and Systems   (1.5)', 'ECE310: Digital Signal Processing I   (1.5)', 'ECON180: Introduction to Economics and Financial Project Evaluation   (1.5)', 'MATH122: Logic and Foundations   (1.5)', 'SENG265: Software Development Methods   (1.5)', 'SENG275: Software Testing   (1.5)', 'SENG310: Human Computer Interaction   (1.5)', 'STAT260: Introduction to Probability and Statistics I   (1.5)', 'Complete  3.0  units of:  Complementary Studies Electives (see note below)', 'CSC226: Algorithms and Data Structures II   (1.5)', 'CSC320: Foundations of Computer Science   (1.5)', 'CSC360: Operating Systems   (1.5)', 'CSC370: Database Systems   (1.5)', 'SENG426: Software Quality Engineering   (1.5)', 'SENG440: Embedded Systems   (1.5)', 'SENG499: Design Project II   (3)']
    courses = ["CSC225: Algorithms and Data Structures I   (1.5)"
]
    course_comp = [
    # 1st Year
    "CSC111: Fundamentals of Programming with Engineering Applications   (1.5)",
    "CSC115: Fundamentals of Programming II   (1.5)",

    # 2nd Year
    "CSC225: Algorithms and Data Structures I   (1.5)",
    "CSC230: Introduction to Computer Architecture   (1.5)",  # or ECE255
    "ECE260: Continuous-Time Signals and Systems   (1.5)",
    "ECE310: Digital Signal Processing I   (1.5)",
    "MATH122: Logic and Foundations   (1.5)",
    "SENG265: Software Development Methods   (1.5)",
]
    
    course_codes = []
    for c in course_comp:
        match = re.match(r"[A-Z]{3,4}\d{3}", c)
        if match:
            course_codes.append(match.group(0))

    avail = True
    for course in courses:
        pre_reqs = await pre_req_fetch(course)
        # course_c = re.match(r"[A-Z]{3,4}\d{3}", course).group(0)

        for pre in pre_reqs:
            if "Complete 1 of" == pre['type']:
                if not any(c in pre['courses'] for c in course_codes):
                    avail = False
                    # print(course," can be done by user")
                    # print(pre)
                    # print(" ")
        if avail==False:
            print(f"{course} cannot be dne by user")
        else:
             print(f"{course} can be dne by user")


    return 0

if __name__ == "__main__":
    import asyncio
    asyncio.run(pre_req_check())