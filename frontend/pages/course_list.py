import streamlit as st

st.title("Course List")

# Example course list
courses = [
    "CSC 110 - Fundamentals of Programming",
    "CSC 115 - Introduction to Programming II",
    "CSC 225 - Algorithms and Data Structures I",
    "CSC 226 - Algorithms and Data Structures II",
    "CSC 230 - Computer Architecture",
    "CSC 305 - Databases and Information Management",
    "CSC 349 - Computational Intelligence",
    "CSC 360 - Operating Systems",
    "CSC 370 - Computer Graphics",
    "CSC 375 - Introduction to Data Analytics",
    "CSC 405 - Advanced Database Topics",
    "CSC 460 - Advanced Operating Systems",
    "CSC 461 - Computer Communications and Networks",
    "CSC 462 - Introduction to Network Security",
    "CSC 464 - Introduction to Cryptography",
    "CSC 467 - Internet of Things and Cyber-Physical Systems",
    "CSC 475 - Machine Learning",
    "CSC 485 - Special Topics in Computer Science",
    "MATH 100 - Calculus I",
    "MATH 101 - Calculus II",
    "MATH 122 - Logic and Foundations",
    "MATH 211 - Matrix Algebra II",
    "STAT 260 - Introduction to Probability and Statistics for Engineers",
    "PHYS 110 - Introductory Physics I",
    "PHYS 111 - Introductory Physics II",
    "ENGL 135 - Academic Reading and Writing"
]



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
        st.switch_page("pages/chatbot.py")
