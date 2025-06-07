from dotenv import load_dotenv
load_dotenv()  # ✅ Must come before any os.getenv() calls

from fastapi import FastAPI
from .db import database, init_db
from .api.decode import router as extract_courses_router
from .api.course_complete import router as courses_completed
from .api.cohere_chat import router as cohere_router
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()
# Load .env variables
load_dotenv()

print("✅ COHERE_API_KEY =", os.getenv("COHERE_API_KEY"))

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
    

# include your existing routers
app.include_router(extract_courses_router)
app.include_router(courses_completed)
app.include_router(cohere_router)
# app.include_router(courses__not_completed)