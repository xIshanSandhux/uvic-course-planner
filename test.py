# import json
# import re

# # 1. Load the JSON file
# with open('courses.json', 'r', encoding='utf-8') as f:
#     courses = json.load(f)

# # 2. Locate CSC 225
# csc225 = next(course for course in courses if course.get('__catalogCourseId') == 'CSC370')

# # 3. Extract the raw prereq HTML/text
# raw = csc225.get('preAndCorequisites', '')  # or 'preAndCorequisites'
# # print(raw)

# # 4. Strip HTML tags (if any) to get plain text
# clean = re.sub(r'<[^>]+>', '', raw)

# # 5. Optionally, parse out course codes with regex
# prereqs = re.findall(r'[A-Z]{3}\s*\d{3}|[A-Z]{4}\s*\d{3}', clean)

# print('Prerequisites for CSC 225:', prereqs)

import json
import re
from bs4 import BeautifulSoup

def parse_prerequisites(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    groups = []
    seen = set()

    for div in soup.select('div[data-test$="-result"]'):
        text = div.get_text(" ", strip=True)

        # Detect type
        if "Complete all of" in text:
            rule_type = "AND"
            count = None
        else:
            m = re.search(r'Complete\s+(\d+)\s+of', text)
            if m:
                rule_type = "OR"
                count = int(m.group(1))
            else:
                continue  # Not a recognized prereq block

        ul = div.find_next('ul')
        if not ul:
            continue

        opts = []
        for li in ul.find_all('li', recursive=False):
            a = li.find('a')
            if a:
                code = a.get_text(strip=True)
            else:
                code = li.get_text(" ", strip=True)
            if code and code not in seen:
                opts.append(code)
                seen.add(code)

        groups.append((rule_type, count, opts))

    return groups

# ——— Example usage ———

with open('courses.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

csc370 = next(c for c in courses if c['__catalogCourseId'] == 'SENG468')
groups = parse_prerequisites(csc370['preAndCorequisites'])

for rule_type, count, opts in groups:
    if rule_type == "AND":
        print(f"Must complete all of: {', '.join(opts)}")
    else:
        print(f"Must complete {count} of: {', '.join(opts)}")
