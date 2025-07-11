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
        print(course['course_code'])
        if match:
            subject = match.group(1)
            number = match.group(2)
            print(f"Subject: {subject}, Number: {number}")
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
            print("course avail this term")
        elif data['totalCount']==0:
            avail = False
            print("course not avail this term")

        await context.close()
        return avail
    

# returns the list of courses which are not completed by the user and are offered in the term
# @router.get("/courses_not_completed")
async def course_not_comp():
    await database.connect()
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
    # print(course_not_comp)
    course_avail =[]
    for course in course_not_comp:
        match = re.search(r"\b[A-Z]{3,4}\d{3}\b", course)
        if match:
            query = select(courses_main).where(courses_main.c.course_code == match.group(0))
            course_db = await database.fetch_one(query)
            if course_db['Summer'] is True:
                print(course)
                course_avail.append(course)
        else:
            course_avail.append(course)
    
    print(course_avail)
    # return course_avail
        

# # ✅ Run the async function
asyncio.run(course_not_comp())


# if __name__ == "__main__":
#     init_db()
