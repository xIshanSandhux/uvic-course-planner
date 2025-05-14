import os
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON
from databases import Database
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)
metadata = MetaData()

# Single table for course data including a prerequisites list
courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("catalog_course_id", String, unique=True, index=True),
    Column("pid", String, index=True),
    Column("title", String),
    Column("credits", Integer),
    Column("major", String),
    Column("prerequisites", JSON),  # List of prerequisite catalog_course_ids
    Column("raw_json", JSON),
)

courses_main = Table(
    "courses_main",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pid", String, index=True, unique=True),
    Column("course_code", String, nullable=True, index=True),
    Column("course_name", String, nullable=True),
    Column("course_description", String, nullable=True),
    Column("prerequisites", JSON, nullable=True),  # List of prerequisite
    Column("credits", Integer, nullable=True),
)

majors = Table(
    "majors",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("major", String, unique=True, index=True),
    Column("major_pid", String, index=True),
    Column("courses", JSON),
)

def init_db():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
