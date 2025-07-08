from dotenv import load_dotenv
from fastapi import FastAPI
from .db import database, init_db
from .api.courses.extract_courses import router as extract_courses_router
from .api.courses.course_complete import router as courses_completed_and_not_completed
from .api.llm.cohere_chat import router as cohere_router
from .api.llm.google_gemma_chat import router as google_gemma_chat_router
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()
# Load .env variables
load_dotenv()

# print("COHERE_API_KEY =", os.getenv("COHERE_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] for stricter rules
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # 1) ensure the tables exist (safe to run every time)
    init_db()
    # 2) open your async Database connection
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    # cleanly close your DB connection
    await database.disconnect()
    

# extract_courses_router: /extract_courses
# courses_completed_and_not_completed: /courses_completed, /course_list, /courses_not_completed
# cohere_router: /cohere_chat
app.include_router(extract_courses_router)
app.include_router(courses_completed_and_not_completed)
app.include_router(cohere_router)
app.include_router(google_gemma_chat_router)