from fastapi import FastAPI
from .db import database, init_db
from .api.decode import router as extract_courses_router
from .api.course_complete import router as courses_completed
# import os
# from supabase import create_client, Client

app = FastAPI()
# Load .env variables
# load_dotenv()

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