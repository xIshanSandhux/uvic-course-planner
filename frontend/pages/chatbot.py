import random
import time
import streamlit as st
from io import BytesIO
from openai import AzureOpenAI
import requests


courses_completed =  requests.get("http://127.0.0.1:8000/courses_completed")
courses_com = courses_completed.json()
course_all = (requests.get("http://127.0.0.1:8000/course_list")).json()
print("courses: ",courses_com)

# --- PAGE SETTINGS ---
st.set_page_config(
    page_title="UVic Course Planner",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("UVic Course Planner AI Assistant")

# --- GET USER INFO ---
user_name = st.session_state.get('name')  # Safe fallback if 'name' is missing

# Azure OpenAI client Initialization
client = AzureOpenAI(
    api_key= st.secrets["AZURE_OPENAI_API_KEY"],
    azure_endpoint= st.secrets["AZURE_OPENAI_ENDPOINT"],
    api_version= st.secrets["AZURE_OPENAI_API_VERSION"]
)


major = st.session_state.get('major', 'an unspecified major')
minor = st.session_state.get('minor', '')
specialization = st.session_state.get('specialization', '')
interests = st.session_state.get('interests', 'general academic fields')
year = st.session_state.get('year', 'an unspecified year')
number_of_courses = st.session_state.get('number of courses','0')
name = st.session_state.get('name')
elective_courses = st.session_state.get('elective_courses')
core_courses = st.session_state.get('core_courses')

# Handle minor
if minor:
    minor_sentence = f"They have a minor in {minor}."
else:
    minor_sentence = "They do not have a minor."

if major == "Select a major":
    major_sentence = "They have an unspecified major."
elif major:
    major_sentence = f"They have a major in {major}."

# Handle specialization
if specialization:
    specialization_sentence = f"They have a specialization in {specialization}."
else:
    specialization_sentence = "They have no specialization."

extra_instructions = "There are not extra instructions."

# Different instructions based on year
if year == "First Year":
    extra_instructions = "Focus on suggesting introductory-level courses, core program requirements, and electives that do not have heavy prerequisites. Be very encouraging and explain options simply."
elif year == "Second Year":
    extra_instructions = "Suggest a mix of core required courses and some elective options. Assume the student has completed most first-year prerequisites."
elif year == "Third Year":
    extra_instructions = "Suggest advanced electives and core upper-level courses. Help them explore specialization options if they are still open."
elif year == "Fourth Year":
    extra_instructions = "Focus on suggesting capstone projects, technical electives, and courses that complete graduation requirements."

coop_completed = st.session_state.get("coop_completed", 0)
coop_planned   = st.session_state.get("coop_planned", 0)


# Courses 

# Now create the full system prompt
system_prompt = f"""
You are a kind and helpful UVic course planning assistant expert.
{major_sentence}
{minor_sentence}
{specialization_sentence}
Their academic interests include {interests}. Courses completed by the user are {courses_com}.
They are currently in their {year} of study. Course list of the user's major is {course_all}
They want to take {elective_courses} number of elective courses.
They want to take {core_courses} number of core courses.
{extra_instructions}

Note: The student has completed {coop_completed} co-op term{"s" if coop_completed != 1 else ""} and plans to complete {coop_planned}. 
Since they’re looking to do more co-op, you can either tailor course suggestions around that or direct them to explore co-op applications at https://learninginmotion.uvic.ca/.

Always ensure prerequisites are met, workloads are balanced, and their interests are supported.
Speak in a friendly and encouraging tone. Personalize your responses by addressing the student by their name: {name}.
"""


# Set default model deployment name
st.session_state["openai_deployment"] = st.secrets["AZURE_OPENAI_DEPLOYMENT"]   # <-- Important! Set your deployment name

# Initialize chat messages if not already
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    full_message =  [{"role": "system", "content": system_prompt}] + [
    {"role": m["role"], "content": m["content"]}
    for m in st.session_state.messages
    ]

    # Assistant reply
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_deployment"],  # Use deployment name, not model name
            messages=full_message,
            stream=True,
        )
        response = st.write_stream(stream)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})