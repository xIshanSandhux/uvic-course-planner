import io
import streamlit as st
import http.client
import json
from openai import AzureOpenAI
import requests
import re
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Create router
router = APIRouter()

courses_completed = []
courses_completed_str =""
courses_not_completed = []

if "course_completed" not in st.session_state:
    st.session_state['course_completed'] = ""
if "full_course_list" not in st.session_state:
    st.session_state['full_course_list'] = ""

class ExtractRequest(BaseModel):
    courses: list

@router.post("/courses_completed")
def courses_completed(req:ExtractRequest):
    try:
        courses_completed = req.courses
        courses_completed_str = ", ".join(courses_completed)
        st.session_state['course_completed'] = courses_completed_str
        # print(courses_completed_str)
    except Exception as e:
        return {"error": str(e)}

@router.get("/courses_completed")
def courses_completed():
    try:
        # print("get request ",courses_completed_str)
        return st.session_state['course_completed']
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/course_list")
def full_course_list(req:ExtractRequest):
    try:
        courses_list = ", ".join(req.courses)
        st.session_state['full_course_list'] = courses_list
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/course_list")
def full_course_list():
    try:
        # print("get request ",st.session_state['full_course_list'])
        return st.session_state['full_course_list']
    except Exception as e:
        return {"error": str(e)}
