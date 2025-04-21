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


load_dotenv()


# Create router
router = APIRouter()


class ExtractRequest(BaseModel):
    major: str

# Getting all the required links from the webpage
def searching_ppw(major:str):

    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    "q": f"univeristy of victoria ppw for the major {major}"
    })
    headers = {
    'X-API-KEY': os.getenv("SEARCH_API_KEY"),
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    # read, decode, load JSON
    data = res.read()
    # decoding into json response
    text = data.decode("utf-8")
    # converting into dictionary
    parsed = json.loads(text)
    # getting the main json response
    organic = parsed["organic"]

    # extracting only title,link and snippet
    search_results_text = "\n\n".join(
        [f"Title: {item['title']}\nLink: {item['link']}\nSnippet: {item['snippet']}" for item in organic]
    )

    return search_results_text

# picking the best link using AzureOpenAI
def picking_pdf_link(search_results_text:str,major:str):


    client = AzureOpenAI(
        api_key= os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=  os.getenv("AZURE_OPENAI_API_VERSION")
    )

    prompt = f"""
    You are a helpful assistant.

    Below are search results related to UVic Program Planning Worksheet (PPW) for the major {major}.

    {search_results_text}

    Your task:
    - Find the link that points to the official Program Planning Worksheet(PPW) for the major {major} at UVic.
    - Prefer links hosted on the uvic.ca domain.
    - Prefer PDF documents (.pdf).
    - Ignore Reddit, CourseHero, Scribd, or unofficial websites.
    - Reply ONLY with the correct URL (no explanation, no extra text).
    """

    # setting temp to 0 so that llm gives me deterministic outputs 
    response = client.chat.completions.create(
        model="gpt-4o-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )

    link_latest = response.choices[0].message.content.strip()

    print("Best pdf course link: ",link_latest)
    return link_latest

def extracting_courses(link:str):

    resp = requests.get(link)
    pdf_bytes = io.BytesIO(resp.content)

    document_analysis_client = DocumentAnalysisClient(
        endpoint=os.getenv("AZURE_PDF_EXTRACT_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_PDF_EXTRACT_API_KEY"))
    )

    poller = document_analysis_client.begin_analyze_document(
        model_id="prebuilt-layout", document=pdf_bytes
    )

    result = poller.result()

    extracted_lines = []
    buffer_line = ""

    for page in result.pages:
        for line in page.lines:
            line_text = line.content.strip()

            if not buffer_line:
                buffer_line = line_text
            else:
                if line_text.lower().startswith("or "):
                    # Stitch 'or' line to previous
                    buffer_line += " " + line_text
                else:
                    # New line, save previous
                    extracted_lines.append(buffer_line)
                    buffer_line = line_text

    # Add last buffer line if any
    if buffer_line:
        extracted_lines.append(buffer_line)

    # Step 4: Now filter lines that contain course codes
    final_course_mentions = [
        line for line in extracted_lines if re.search(r'[A-Z]{3,4}\s\d{3}|\b[1-5]{1,5}\sTechnical Electives\b|\bNatural Science\b|\bComplementary Studies\b', line)
    ]

    # Step 5: Output
    print("Extracted course mentions (stitched):")
    for item in final_course_mentions:
        print("-", item)

    return final_course_mentions


# main API
@router.post("/extract_courses")
def extracted_courses(req:ExtractRequest):

    try:
        # initial_links = searching_ppw(req.major)
        # actual_link = picking_pdf_link(initial_links,req.major)
        # courses = extracting_courses(actual_link)
        courses = extracting_courses("https://www.uvic.ca/ecs/_assets/docs/program-planning/PPW-SENG.pdf")
        return courses
        # print()
    except Exception as e:
        return {"error": str(e)}