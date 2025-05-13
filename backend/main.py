from fastapi import FastAPI
from .db import database, init_db
from .api.decode import router as extract_courses_router
from .api.course_complete import router as courses_completed

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_db()
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Include all routers
app.include_router(extract_courses_router)
app.include_router(courses_completed)

# app.include_router(another_router)  # (optional if you have more)
