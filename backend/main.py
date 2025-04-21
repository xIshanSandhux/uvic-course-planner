from fastapi import FastAPI
from backend.api.scrap import router as extract_courses_router

# from api.another_api import router as another_router  # (if you have more)

app = FastAPI()

# Include all routers
app.include_router(extract_courses_router)
# app.include_router(another_router)  # (optional if you have more)
