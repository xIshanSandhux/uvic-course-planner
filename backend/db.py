# backend/db.py
import os
import sqlalchemy
from sqlalchemy import (
    Table, Column, Integer, String, JSON, MetaData, ForeignKey
)
from databases import Database
from dotenv import load_dotenv


load_dotenv()  # so DATABASE_URL is picked up

DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)
metadata = MetaData()

# courses table
courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("catalog_course_id", String, unique=True, index=True),
    Column("pid", String, index=True),
    Column("title", String),
    Column("credits", Integer),
    Column("major", String),
    Column("raw_json", JSON),
)

# prerequisites table
prerequisites = Table(
    "prerequisites",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("course_id", String, ForeignKey("courses.catalog_course_id")),
    Column("prereq_catalog_id", String),
)

def init_db():
    """Create tables if they don’t exist."""
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
