import json
import html
from bs4 import BeautifulSoup
import csv

def extract_courses_from_json(json_path):
    # Load and decode JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    decoded_program = data["programRequirements"].encode().decode('unicode_escape')
    clean_program = html.unescape(decoded_program)

    # Parse the HTML
    soup = BeautifulSoup(clean_program, 'html.parser')

    course_list = []

    # Loop through all <li> tags
    for li in soup.find_all('li'):
        # ✅ Only process leaf <li> (no inner <ul>)
        if not li.find('ul'):
            a_tag = li.find('a')
            if a_tag and a_tag.text.strip():
                # CASE 1️⃣: Course with <a> tag
                course_code = a_tag.text.strip()
                full_text = li.get_text(" ").strip()

                # Clean up: remove course code from text
                if full_text.startswith(course_code):
                    rest_of_text = full_text[len(course_code):].strip(" -–:")
                else:
                    rest_of_text = full_text  # fallback

                course_list.append((course_code, rest_of_text))

            else:
                # CASE 2️⃣: No <a> tag, it's a plain text elective
                elective_text = li.get_text(" ").strip()
                course_list.append(("Elective/Requirement", elective_text))

    # Remove duplicates while preserving order
    course_list = list(dict.fromkeys(course_list))

    return course_list

def print_courses(course_list):
    for code, title in course_list:
        print(f"{code}: {title}")

def save_courses_to_csv(course_list, output_path='courses.csv'):
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Course Code / Type', 'Course Title / Requirement'])
        writer.writerows(course_list)
    print(f"\n✅ Saved {len(course_list)} items to {output_path}")

if __name__ == "__main__":
    json_file = 'data.json'  # Path to your JSON file
    courses = extract_courses_from_json(json_file)

    # Print to console
    print_courses(courses)

    # Optional: Save to CSV
    # save_courses_to_csv(courses)
