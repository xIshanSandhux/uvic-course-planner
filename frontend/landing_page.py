import streamlit as st


st.set_page_config(
    page_title="UVic Course Planner",
    page_icon="🎓",
    layout="centered",  # Keep centered for a clean form
    initial_sidebar_state="collapsed",  # Sidebar open by default
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("UVic Course Planner 🎓")

st.write("""
Welcome to the UVic Course Planner, an AI-powered assistant to help you:
- Pick your courses smartly
- Avoid conflicts in schedule
- Get suggestions based on your interests
- Generate and export timetables easily
""")

if st.button("Start Planning"):
    st.switch_page("pages/user_pref.py")