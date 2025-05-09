from pathlib import Path
import asyncio
from playwright.async_api import async_playwright

async def run():
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
        await page.fill(".select2-input", "SENG")
        await page.click("#SENG")

        # 7️⃣ Enter the course number
        await page.fill("#txt_courseNumber", "426")

        # 8️⃣ Click the Search button
        await page.click("#search-go")

        await asyncio.sleep(10)

        # 🚀 9️⃣ Open a new tab in the SAME WINDOW + SESSION
        new_page = await context.new_page()
        await new_page.goto("https://banner.uvic.ca/StudentRegistrationSsb/ssb/searchResults/searchResults")

        await asyncio.sleep(15)

        await context.close()

# ✅ Run the async function
asyncio.run(run())
