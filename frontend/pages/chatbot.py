import random
import time
import streamlit as st
from io import BytesIO
from openai import AzureOpenAI
import requests
import cohere

# --- PAGE SETTINGS ---
st.set_page_config(
    page_title="UVic Course Planner",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("UVic Course Planner AI Assistant")

# courses_completed =  requests.get("http://127.0.0.1:8000/courses_completed")
# courses_com = courses_completed.json()
# course_all = (requests.get("http://127.0.0.1:8000/course_list")).json()
# print("courses: ",courses_com)

@st.cache_data
def get_courses_completed():
    return requests.get("http://127.0.0.1:8000/courses_completed").json()

@st.cache_data
def get_course_list():
    return requests.get("http://127.0.0.1:8000/course_list").json()

courses_com = get_courses_completed()
course_all = get_course_list()

# --- GET USER INFO ---
user_name = st.session_state.get('name')  # Safe fallback if 'name' is missing

# Cohere client Initialization
client = cohere.Client(st.secrets["COHERE_API_KEY"])


major = st.session_state.get('major', 'an unspecified major')
minor = st.session_state.get('minor', '')
specialization = st.session_state.get('specialization', '')
interests = st.session_state.get('interests', 'general academic fields')
year = st.session_state.get('year', 'an unspecified year')
number_of_courses = st.session_state.get('number of courses','0')
name = st.session_state.get('name')
elective_courses = st.session_state.get('elective_courses', 0)
core_courses = st.session_state.get('core_courses', 0)

# Handle minor
if minor:
    minor_sentence = f"They have a minor in {minor}."
else:
    minor_sentence = "They do not have a minor."

if major == "Select a major":
    major_sentence = "They have an unspecified major."
elif major:
    major_sentence = f"They have a major in {major}."

# Majors that require technical, complementary, and/or natural science electives 
eng_majors = [
"Software Engineering",
"Electrical Engineering",
"Computer Engineering",
"Biomedical Engineering",
"Mechanical Engineering",
"Civil Engineering",
]

# If their major is eng, add elective question
extra_major_prompt = "No additional major-related questions."
if major in eng_majors:
    extra_major_prompt = (
        "How many technical, complementary, and/or natural science electives would you like to take this term?"
    )

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
You are a kind and helpful UVic course planning assistant expert. If you need additional information, you can ask them before providing the most accurate possible recommendation/help.
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

Possible questions to ask:
{extra_major_prompt}

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

# Show welcome message if no messages yet
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("👋 Hi! I'm your UVic course planning assistant. Ask me anything about course selection!")
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hi! I'm your UVic course planning assistant. Ask me anything about course selection!"
    })

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
    chat_history = [{"role": "SYSTEM", "message": system_prompt}] + [
        {
            "role": "USER" if m["role"] == "user" else "CHATBOT",
            "message": m["content"]
        }
        for m in st.session_state.messages
    ]

    try:
        response = client.chat(
            message=prompt,
            model="command-r",
            chat_history=chat_history
        )
        st.chat_message("assistant").markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")