# source venv/bin/activate
# python3 -m venv venv
import streamlit as st

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

st.session_state['number_of_courses'] = st.slider('How many courses do you want to take?', 1, 6, value=st.session_state['number_of_courses'])

st.session_state['degree_type'] = st.selectbox("Select your Degree Type", 
    ["Please Select an Option", "Undergraduate", "Master", "PHD"],
    index=["Please Select an Option", "Undergraduate", "Master", "PHD"].index(st.session_state['degree_type'])
)

st.session_state['student_status'] = st.selectbox("Have you completed any courses at UVic or have transfer credits for courses?", 
    ["Please Select an Option", "Yes", "No"],
    index=["Please Select an Option", "Yes", "No"].index(st.session_state['student_status'])
)

# Maybe add faculty ? and then narrow down major based on faculty? 
# need to figure out a way to the current date. prolly streamlit should have a way to get the current date
# if it is summer currently display option for fall and spring term
# if it is fall currently then just display 
# term = st.selectbox("Which term are you planning for?", ["Fall", "Spring", "Summer"])

# Saving info for the session
# st.session_state['name'] = name



# Clicking next button
if st.button("Next"):
    if st.session_state['student_status']=="Yes":
        # print("Name: ",st.session_state['name'])
        # print("Major: ",st.session_state['major'])
        # print("Minor: ",st.session_state['minor'])
        # print("Specialization: ",st.session_state['specialization'])
        # print("Number of Courses: ",st.session_state['number_of_courses'])
        # print("Student status: ",st.session_state['student_status'])
        # print("Degree Type: ",st.session_state['degree_type'])
        
        st.switch_page("pages/course_list.py")

    elif st.session_state['student_status']=="No" :
        # print("Name: ",st.session_state['name'])
        # print("Major: ",st.session_state['major'])
        # print("Minor: ",st.session_state['minor'])
        # print("Specialization: ",st.session_state['specialization'])
        # print("Number of Courses: ",st.session_state['number_of_courses'])
        # print("Student status: ",st.session_state['student_status'])
        # print("Degree Type: ",st.session_state['degree_type'])

        st.switch_page("pages/chatbot.py")




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


    

