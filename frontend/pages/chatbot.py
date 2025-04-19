import random
import time
import streamlit as st
from io import BytesIO


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

# --- Streamed Response Emulator ---
def response_generator(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.6)

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # --- Assistant starts the conversation! ---
    welcome_message = f"Hello {user_name}! 🎓 Let's get started planning your courses!"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# --- Display chat messages from history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Accept user input ---
if prompt := st.chat_input("What is up?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    assistant_reply = random.choice(
        [
            f"Thanks for your question, {user_name}! Let me help you with that.",
            f"Alright {user_name}, let me find the best schedule for you!",
            f"Good question! Here's what I suggest...",
        ]
    )

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(assistant_reply))
    
    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

