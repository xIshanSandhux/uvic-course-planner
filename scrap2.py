import asyncio
from playwright.async_api import async_playwright

URL = "https://www.uvic.ca/calendar/undergrad/index.php#/programs"

async def scrape_program_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(URL)
        await asyncio.sleep(6)

        # Wait for the program list to load
        # await page.wait_for_selector('li.style_item__1ew0K')

        locator = page.locator('li.style__item___1ewOk')

        count = await locator.count()
        print(count)

        for i in range(count):
            item = locator.nth(i)

            # FIX: pick only the first <a>
            link_el = item.locator('a').first
            
            name = await link_el.inner_text()
            relative_link = await link_el.get_attribute('href')
            full_link = f"{relative_link}"

            print(f"{i} {name}: {full_link}")



        # # Extract all program list items
        # list_items = await page.query_selector_all('li.style__item___1ewOk')
        # 
        # print(list_items)

        # programs = []
        # for item in list_items:
        #     # Find <a> tag inside each item
        #     link_el = await item.query_selector('a')
        #     if link_el:
        #         name = await link_el.inner_text()
        #         relative_link = await link_el.get_attribute('href')
        #         full_link = f"https://www.uvic.ca/calendar/undergrad/index.php{relative_link}"

        #         # Try to get the type (Certificate, Minor, etc.)
        #         type_span = await item.query_selector('span.style__extension__3fbic')
        #         program_type = await type_span.inner_text() if type_span else ''

        #         programs.append({
        #             'name': name.strip(),
        #             'link': full_link,
        #             'type': program_type.strip()
        #         })

        # # Print results
        # for prog in programs:
        #     print(f"{prog['name']} ({prog['type']}): {prog['link']}")

        await browser.close()

# Run it
asyncio.run(scrape_program_links())
