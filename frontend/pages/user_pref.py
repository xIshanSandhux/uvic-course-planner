# source venv/bin/activate
# python3 -m venv venv
# pip install -r requirement.txt
import streamlit as st
import requests

st.set_page_config(
    page_title="UVic Course Planner",
    page_icon="🎓",
    layout="centered",  # Keep centered for a clean form
    initial_sidebar_state="collapsed",  # Sidebar open by default
)

# Title and header
st.title("UVic Course Planner 🎓")
st.header("User Details")

# Initalizing session state
if "name" not in st.session_state:
    st.session_state['name'] = ""
if "major" not in st.session_state:
    st.session_state['major'] = "Select a Major"
if "prev_major" not in st.session_state:
    st.session_state['prev_major']= ""
if "minor" not in st.session_state:
    st.session_state['minor'] = ""
if "specialization" not in st.session_state:
    st.session_state['specialization'] = ""
if "number_of_courses" not in st.session_state:
    st.session_state['number_of_courses'] = 1
if "student_status" not in st.session_state:
    st.session_state['student_status'] = "Please Select an Option"
if "degree_type" not in st.session_state:
    st.session_state['degree_type'] = "Please Select an Option"
if "year" not in st.session_state:
    st.session_state['year'] = "Please Select an Option"
if "courses" not in st.session_state:
    st.session_state['courses'] = []
if "core_courses" not in st.session_state:
    st.session_state['core_courses'] = 1
if "elective_courses" not in st.session_state:
    st.session_state['elective_courses'] = 0

# name = st.text_input("Name", placeholder="Enter your name", value=st.session_state['name'])
# major = st.selectbox("Select your major", ["Select a Major","Software Engineering", "Computer Science", "Electrical Engineering","Computer Engineering","Biomedical Engineering","Mechanical Engineering","Civil Engineering"])
# minor = st.text_input("Enter your Minor",placeholder="e.g., Business, Biology",value=st.session_state['minor'])
# specialization = st.text_input("Specialization (optional)", placeholder="e.g., AI, Cybersecurity",value=st.session_state['specialization'])
# num_courses = st.slider('How many courses do you want to take?', 1, 3, 6)
# deg_type = st.selectbox("Select your Degree Type",["Please Select an Option","Undergraduate","Master","Phd"],value=st.session_state['student_status'])
# student_status = st.selectbox("Have you completed any courses at UVic or have transfer credits for courses?",["Please Select an Option","Yes","No"],value=st.session_state['degree_type'])

st.session_state['name'] = st.text_input("Name", value=st.session_state['name'], placeholder="Enter your name")

st.session_state['major'] = st.selectbox("Select your major", 
    ["Select a Major", "Software Engineering", "Computer Science", "Electrical Engineering", "Computer Engineering", "Biomedical Engineering", "Mechanical Engineering", "Civil Engineering"],
    index=["Select a Major", "Software Engineering", "Computer Science", "Electrical Engineering", "Computer Engineering", "Biomedical Engineering", "Mechanical Engineering", "Civil Engineering"].index(st.session_state['major'])
)

st.session_state['minor'] = st.text_input("Enter your Minor", value=st.session_state['minor'], placeholder="e.g., Business, Biology")

st.session_state['specialization'] = st.text_input("Specialization (optional)", value=st.session_state['specialization'], placeholder="e.g., AI, Cybersecurity")

col1, col2 = st.columns(2)

with col1:
    core = st.slider(
        'How many core courses do you want to take?',
        0, 3, 
        value=st.session_state['core_courses']
    )
    st.session_state['core_courses'] = core

with col2:
    # Calculate remaining slots for electives
    elective = st.slider(
        'How many electives do you want to take?',
        0, 3, 
        value=st.session_state['elective_courses']
    )
    st.session_state['elective_courses'] = elective

total_courses = st.session_state['core_courses'] + st.session_state['elective_courses']
if total_courses >= 8:
    st.warning('Total number of courses cannot exceed 8')

st.session_state['number_of_courses'] = total_courses

st.session_state['degree_type'] = st.selectbox("Select your Degree Type", 
    ["Please Select an Option", "Undergraduate", "Master", "PHD"],
    index=["Please Select an Option", "Undergraduate", "Master", "PHD"].index(st.session_state['degree_type'])
)

st.session_state['student_status'] = st.selectbox("Have you completed any courses at UVic or have transfer credits for courses?", 
    ["Please Select an Option", "Yes", "No"],
    index=["Please Select an Option", "Yes", "No"].index(st.session_state['student_status'])
)
st.session_state['year'] = st.selectbox("What year are you in?", 
    ["Please Select an Option", "Year 1", "Year 2", "Year 3","Year 4"],
    index=["Please Select an Option", "Year 1", "Year 2", "Year 3","Year 4"].index(st.session_state['year'])
)

# Maybe add faculty ? and then narrow down major based on faculty? 
# need to figure out a way to the current date. prolly streamlit should have a way to get the current date
# if it is summer currently display option for fall and spring term
# if it is fall currently then just display 
# term = st.selectbox("Which term are you planning for?", ["Fall", "Spring", "Summer"])



# Extracting the course list of the student
course_list = []
major = st.session_state['major']
print(major)
prev_major = st.session_state['prev_major']
print(prev_major)
# or st.session_state['courses'] == []
if (prev_major!= major and major != "Select a Major"):
        try:
            response = requests.post("http://127.0.0.1:8000/extract_courses", json={"major": major})
            print("code:", response.status_code)
            if response.status_code == 200:
                data = response.json()
                # print("data:", data)

                # check if response is a list (courses) or dict (error)
                if isinstance(data, list):
                    print(data)
                    st.session_state['courses'] = data
                    st.success("Courses extracted successfully!")
                elif isinstance(data, dict):
                    # API returned an error dictionary
                    st.error(f"Error: {data.get('error', 'Unknown error')}")
                else:
                    st.error("Unexpected response format from backend.")
            else:
                st.error(f"Backend error: {response.status_code}")
        except Exception as e:
            st.error(f"Error contacting backend: {e}")
        st.session_state['prev_major'] = major

# st.session_state['courses'] = course_list
print(st.session_state['courses'])

if st.session_state['courses'] !=[] or st.session_state['major']!="Select a Major":
    next_button = st.button("Next")
    if next_button:
        requests.post("http://127.0.0.1:8000/course_list", json={"courses": st.session_state['courses']})
        if st.session_state['student_status']=="Yes":
            st.switch_page("pages/course_list.py")

        elif st.session_state['student_status']=="No" :
            st.switch_page("pages/chatbot.py")
else:
    st.write("Please select a major to continue.")

    # st.error("Please select a major")

# Clicking next button
# try:
#     if next_button:
#         if st.session_state['student_status']=="Yes":
#             st.switch_page("pages/course_list.py")

#         elif st.session_state['student_status']=="No" :
#             st.switch_page("pages/chatbot.py")
# except Exception :
#     st.error("Please select a major")




# Below is the code if you want in the format of a form

# with st.form("course_form"):
#     name = st.text_input("Enter your name")
#     # Maybe add faculty ? and then narrow down major based on faculty? 

#     major = st.selectbox("Select your major", ["Select a Major","Software Engineering", "Computer Science", "Electrical Engineering","Computer Engineering","Biomedical Engineering","Mechanical Engineering","Civil Engineering"])
#     num_courses = st.slider('How many courses do you want to take?', 1, 3, 6)
#     minor = st.text_input("Enter your Minor",placeholder="e.g., Business, Biology")
#     specialization = st.text_input("Specialization (optional)", placeholder="e.g., AI, Cybersecurity")
#     student_status = st.selectbox("Have you completed any courses at UVic?",["Please Select an Option","Yes","No"])

#     # need to figure out a way to the current date. prolly streamlit should have a way to get the current date
#     # if it is summer currently display option for fall and spring term
#     # if it is fall currently then just display 
#     # term = st.selectbox("Which term are you planning for?", ["Fall", "Spring", "Summer"])

#     # Submit button
#     submit = st.form_submit_button("Next")

#     if submit:
#         print("hel button click")
#         st.success("button clicked")
#     # Need to add error messages later on


    

