from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
import json
import re
import requests


# def course_not_comp():
#     courses_completed = requests.get("http://127.0.0.1:8000/courses_completed").text
#     completed_courses_list =  [c.strip() for c in courses_completed.split(",")]
#     # print("hello course compl: ", courses_completed)

#     course_list = requests.get("http://127.0.0.1:8000/course_list").text
#     course_list_l = [c.strip() for c in course_list.split(",")]
#     # print("hello course list: ", lt1)

#     course_not_comp = []
#     for course in course_list_l:
#         if course not in completed_courses_list:
#             course_not_comp.append(course)

#     for course in course_not_comp:
#         match = re.match(r"([A-Z]+)(\d+):", course)
#         if match:
#             subject = match.group(1)
#             number = match.group(2)
#             print(f"Subject: {subject}, Number: {number}")

async def run(subject: str, courseNumber: str):
    async with async_playwright() as p:
        # ✅ 1️⃣ Define the user data directory (profile storage)
        user_data_dir = str(Path.cwd() / "playwright-temp-profile")
        print(f"Using profile: {user_data_dir}")

        # ✅ 2️⃣ Launch *persistent context* for real tabs in one window
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
        )

        # ✅ 3️⃣ Get the first (default) page
        page = context.pages[0]

        # 4️⃣ Go to the search page
        await page.goto("https://banner.uvic.ca/StudentRegistrationSsb/ssb/classSearch/classSearch")

        # 5️⃣ Work with the Term dropdown
        await page.click("#classSearchLink")
        await page.click("#s2id_txt_term")
        await page.fill(".select2-input", "Summer")
        await page.click(r"#\32 02505")
        await page.click("#term-go")

        # 6️⃣ Work with the Subject dropdown
        await page.click("#s2id_txt_subject")
        await page.fill(".select2-input", subject)
        await page.click("#SENG")

        # 7️⃣ Enter the course number
        await page.fill("#txt_courseNumber", courseNumber)

        # 8️⃣ Click the Search button
        await page.click("#search-go")

        # await asyncio.sleep(10)


        new_page = await context.new_page()
        await new_page.goto("https://banner.uvic.ca/StudentRegistrationSsb/ssb/searchResults/searchResults")

        # Wait until the network is idle and content is fully loaded
        await new_page.wait_for_load_state("networkidle")

        # Get the raw JSON string from the body
        raw_json = await new_page.evaluate("document.body.innerText")

        # Parse the JSON using Python
        data = json.loads(raw_json)
        if data['totalCount']>0:
            print("hello")

        await context.close()

# ✅ Run the async function
asyncio.run(run("SENG","426"))
