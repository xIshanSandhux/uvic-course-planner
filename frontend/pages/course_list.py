import streamlit as st

st.title("Course List")

course_list = st.session_state['courses']  # Example: ["CSC 110", "CSC 115", "CSC 110", "ECE 260"]

# --- Initialize checkboxes (only once) ---
for idx, course in enumerate(course_list):
    checkbox_key = f"{course}_{idx}"
    if checkbox_key not in st.session_state:
        st.session_state[checkbox_key] = False

# 🔎 Search bar
search_query = st.text_input("🔍 Search courses:", "")

# 🔥 Filter courses for display
if search_query:
    filtered_courses = [ (idx, course) for idx, course in enumerate(course_list) if search_query.lower() in course.lower()]
else:
    filtered_courses = [ (idx, course) for idx, course in enumerate(course_list)]

# ✅ Show checkboxes
st.write("### Select Courses:")

for idx, course in filtered_courses:
    checkbox_key = f"{course}_{idx}"
    st.checkbox(course, value=st.session_state[checkbox_key], key=checkbox_key)  # 🔥 Only render, don't assign manually!

# 📋 Get all selected courses
selected_courses = []
for idx, course in enumerate(course_list):
    checkbox_key = f"{course}_{idx}"
    if st.session_state.get(checkbox_key):
        selected_courses.append(course)

# ✅ Display selected courses
st.write("### Your Selected Courses:")
if selected_courses:
    for course in selected_courses:
        st.success(course)
else:
    st.info("No courses selected yet.")

print(selected_courses)
