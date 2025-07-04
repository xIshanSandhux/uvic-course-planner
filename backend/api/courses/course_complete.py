# this file has 4 API endpoints:
# 1. /courses_completed: POST request to set the courses completed by the user
# 2. /courses_completed: GET request to get the courses completed by the user
# 3. /course_list: POST request to set the course list for a major
# 4. /course_list: GET request to get the course list for a major
# 5. /courses_not_completed: GET request to get the courses not completed by the user and are offered in the term

import json
import re
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from backend.db import database, courses_main
from pathlib import Path
from playwright.async_api import async_playwright
import asyncio
import sys
import os

# Fix import path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
# from backend.db import database, courses_main, majors

# Create router
router = APIRouter()

# Simulating the session state until we have a proper session management system
class SessionManager:
    def __init__(self):
        self.courses_completed = []
        self.courses_completed_str = ""
        self.courses_not_completed = []
        self.courses_list_str = ""
        self.courses_list = []
        self.pre_req_comp_courses = []
        self.pre_req_comp_str = ""

    def set_courses_completed(self, courses):
        self.courses_completed = courses
        self.courses_completed_str = ", ".join(courses)
    
    def get_courses_completed(self):
        return self.courses_completed_str
    
    def get_courses_completed_list(self):
        return self.courses_completed
    
    def set_courses_not_completed(self, courses):
        self.courses_not_completed = courses
    
    def get_courses_not_completed(self):
        return self.courses_not_completed
    
    def set_courses_list(self, courses):
        self.courses_list = courses
        self.courses_list_str = ", ".join(courses)
    
    def get_courses_list(self):
        return self.courses_list_str

    def set_pre_req_check(self, pre_reqs):
        self.pre_req_comp_courses = pre_reqs

    def get_pre_req_check(self):
        # self.pre_req_comp_str = ", ".join(self.pre_req_comp_courses)
        return self.pre_req_comp_courses


# Pydantic model for the request body
class ExtractRequest(BaseModel):
    courses: list

session = SessionManager()

# POST request to set the courses completed by the user
@router.post("/courses_completed")
def post_courses_completed(req: ExtractRequest):
    try:
        # print(f"Received request: {req}")  # Debug print
        session.set_courses_completed(req.courses)
        # print("courses completed from the frontend: ", session.get_courses_completed())
        return {"message": "Courses completed posted successfully"}
    except Exception as e:
        # print(f"Error in post_courses_completed: {e}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))

# GET request to get the courses completed by the user
@router.get("/courses_completed")
def get_courses_completed():
    try:
        return session.get_courses_completed()
    except Exception as e:
        # print(f"Error in get_courses_completed: {e}")  #
        return {"error": str(e)}

# POST request to set the course list for a major
@router.post("/course_list")
def post_full_course_list(req: ExtractRequest):
    try:
        session.set_courses_list(req.courses)
        # print("course list from the frontend: ", session.get_courses_list())
        return {"message": "Course list posted successfully"}
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

# GET request to get the course list for a major
@router.get("/course_list")
def get_full_course_list():
    try:
        return session.get_courses_list()
    except Exception as e:
        return {"error": str(e)}


# Fetching all the courses form the DB
async def db_courses():
    # await database.connect()
    query = select(courses_main)
    courses = await database.fetch_all(query)
    # await database.disconnect()
    return courses


# calls the both the helper functions to check if the course is offered in the term or not 
async def courses_offered_in_term():
    # await database.connect()
    all_courses = await db_courses()
    course_avail = []

    for course in all_courses:
        match = re.match(r"([A-Z]+)(\d+)", course['course_code'])
        # print(course['course_code'])
        if match:
            subject = match.group(1)
            number = match.group(2)
            # print(f"Subject: {subject}, Number: {number}")
            avail = await run(subject, number)

            query = (
                update(courses_main)
                .where(courses_main.c.pid == course['pid'])
                .values(Summer=avail)
                )
            await database.execute(query)
    # await database.disconnect()
   

# Helper Function which runs the playwright script for each course
# currently only checking if offered in summer 2025
async def run(subject: str, courseNumber: str):
    async with async_playwright() as p:
        # Define the user data directory (profile storage)
        user_data_dir = str(Path.cwd() / "playwright-temp-profile")
        # print(f"Using profile: {user_data_dir}")

        # Launch *persistent context* for real tabs in one window
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
        )

        # Get the first (default) page
        page = context.pages[0]

        # Go to the search page
        await page.goto("https://banner.uvic.ca/StudentRegistrationSsb/ssb/classSearch/classSearch")

        # Work with the Term dropdown
        await page.click("#classSearchLink")
        await page.click("#s2id_txt_term")
        await page.fill(".select2-input", "Summer")
        await page.click(r"#\32 02505")
        await page.click("#term-go")

        # Work with the Subject dropdown
        await page.click("#s2id_txt_subject")
        await page.fill(".select2-input", subject)
        await page.click(f"#{subject}")

        # Enter the course number
        await page.fill("#txt_courseNumber", courseNumber)

        # Click the Search button
        await page.click("#search-go")

        # await asyncio.sleep(10)


        new_page = await context.new_page()
        await new_page.goto("https://banner.uvic.ca/StudentRegistrationSsb/ssb/searchResults/searchResults")

        # Wait until the network is idle and content is fully loaded
        await new_page.wait_for_load_state("networkidle")

        # Get the raw JSON string from the body
        raw_json = await new_page.evaluate("document.body.innerText")
        avail = False
        # Parse the JSON using Python
        data = json.loads(raw_json)
        if data['totalCount']>0:
            avail = True
            # return True
            # print("course avail this term")
        elif data['totalCount']==0:
            avail = False
            # print("course not avail this term")

        await context.close()
        return avail
    

# GET request to get the courses not completed by the user and are offered in the term
@router.get("/courses_not_completed")
async def course_not_comp_get():
    return session.get_courses_not_completed()

@router.post("/courses_not_completed")
async def course_not_comp():
    # await database.connect()
    courses_completed_final = session.get_courses_completed()
    completed_courses_list =  [c.strip() for c in courses_completed_final.split(",")]
    
    course_l = session.get_courses_list()
    course_list_l = [c.strip() for c in course_l.split(",")]
    # print("hello course list: ", lt1)

    course_not_comp = []
    for course in course_list_l:
        if course not in completed_courses_list:
            course_not_comp.append(course)
    # print(course_not_comp)
    course_avail =[]
    for course in course_not_comp:
        match = re.search(r"\b[A-Z]{3,4}\d{3}\b", course)
        if match:
            query = select(courses_main).where(courses_main.c.course_code == match.group(0))
            course_db = await database.fetch_one(query)
            if course_db['Summer'] is True:
                # print(course)
                course_avail.append(course)
        else:
            course_avail.append(course)
    # await database.disconnect()
   

    session.set_courses_not_completed(course_avail)
    return {"message": "Courses not completed posted successfully"}


async def pre_req_fetch(course: str):
    # await database.connect()
    match = re.search(r"\b[A-Z]{3,4}\d{3}\b", course)
    pre_reqs=[]
    if match:
        query = select(courses_main).where(courses_main.c.course_code == match.group(0))
        course_db = await database.fetch_one(query)
        pre_reqs = course_db['prerequisites']
        # print(pre_reqs)
    # await database.disconnect()
    return pre_reqs

# GET request to get the courses not completed by the user and are offered in the term
@router.post("/pre_req_check")
async def pre_req_check():
   
    courses_not_completed = session.get_courses_not_completed()
    # print("courses_not_completed text pre req check: ",courses_not_completed)

    course_comp = session.get_courses_completed_list()
    # print("course_comp text pre req check: ",course_comp)


    course_codes = []
    for c in course_comp:
        match = re.match(r"[A-Z]{3,4}\d{3}", c)
        if match:
            course_codes.append(match.group(0))
    # print("course_codes: ",course_codes)

    avail = True
    prereq_comp = []
    prereq_not_comp = []
    for course in courses_not_completed:

        # print("course: ",course)
        pre_reqs = await pre_req_fetch(course)
        # course_c = re.match(r"[A-Z]{3,4}\d{3}", course).group(0)

        for pre in pre_reqs:
            if "Complete 1 of" == pre['type']:
                if not any(c in pre['courses'] for c in course_codes):
                    avail = False
                    # print(course" can be done by user")
                    # print(pre)
                    # print(" ")
                    if avail==False:
                        # print(f"{course} cannot be dne by user")
                        prereq_not_comp.append(course)
            elif "Complete all of" == pre['type']:
                for c in pre['courses']:
                    if c not in course_codes:
                        avail = False
                        if avail==False:
                            # print(f"{course} cannot be dne by user")
                            prereq_not_comp.append(course)
                            break
        if avail==True:
            prereq_comp.append(course)
            # print(f"{course} can be dne by user")
    # print("prereq_comp: ",prereq_comp)
    # print("prereq_not_comp: ",prereq_not_comp)
    session.set_pre_req_check(prereq_comp)
    print("prereq_comp: ",session.get_pre_req_check())
    return {"message": "Pre-req check posted successfully"}

@router.get("/pre_req_check")
async def pre_req_check_get():
   
    return session.get_pre_req_check()
