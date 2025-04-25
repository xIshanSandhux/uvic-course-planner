import streamlit as st
import requests


if "selected_courses" not in st.session_state:
    st.session_state['selected_courses']=[]

courses = st.session_state['courses']
# --- 🛠 Initialize all course checkbox states ---
for course in courses:
     if course not in st.session_state:
         st.session_state[course] = False
 
 # --- 🔎 Search bar ---
search_query = st.text_input("🔍 Search courses:", "")
 
 # --- 🔥 Filter courses based on search ---
if search_query:
     filtered_courses = [course for course in courses if search_query.lower() in course.lower()]
else:
     filtered_courses = courses
 
 # --- ✅ Show checkboxes for filtered courses ---
st.write("### Select Courses:")

for course in filtered_courses:
    st.checkbox(course, value=st.session_state[course], key=course)   # ❗️ No assignment here

# --- 📋 Get all selected courses ---
selected_courses = [course for course in courses if st.session_state[course]]
# st.session_state['selected_courses'] = selected_courses

# --- 📋 Display selected courses ---
st.write("### Your Selected Courses:")
if selected_courses:
    for course in selected_courses:
        st.success(course)
else:
    st.info("No courses selected yet.")

col1, col2 = st.columns(2)

# Put a button inside each column
with col1:
    if st.button("Back to User Details"):
        st.switch_page("pages/user_pref.py")
with col2:
    if st.button("Start Planning"):
        response = requests.post("http://127.0.0.1:8000/courses_completed", json={"courses": selected_courses})
        st.switch_page("pages/chatbot.py")