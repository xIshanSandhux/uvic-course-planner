# backend/api/decode.py
import html
import json
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..db import database  # relative import from backend/db.py

router = APIRouter()

class ExtractRequest(BaseModel):
    major: str

def get_program_pid(major: str) -> str:
    """Lookup the program pid for a given major title."""
    endpoint = "https://uvic.kuali.co/api/v1/catalog/programs/67855445a0fe4e9a3f0baf82"
    resp = requests.get(endpoint)
    if not resp.ok:
        raise HTTPException(status_code=502, detail="Failed to fetch program list")
    for program in resp.json():
        if program.get("title") == major:
            return program["pid"]
    raise HTTPException(status_code=404, detail=f"Program '{major}' not found")

def parse_program_requirements(pid: str):
    """Fetch & decode the HTML program requirements into code/description pairs."""
    endpoint = f"https://uvic.kuali.co/api/v1/catalog/program/67855445a0fe4e9a3f0baf82/{pid}"
    resp = requests.get(endpoint)
    if not resp.ok:
        raise HTTPException(status_code=502, detail="Failed to fetch program requirements")
    raw_html = resp.json().get("programRequirements", "")
    # Decode escaped unicode + HTML entities
    decoded = raw_html.encode().decode("unicode_escape")
    clean    = html.unescape(decoded)
    soup     = BeautifulSoup(clean, "html.parser")

    courses = []
    for li in soup.find_all("li"):
        # only leaf items (no nested <ul>)
        if li.find("ul"):
            continue

        a_tag = li.find("a")
        if a_tag and a_tag.text.strip():
            code = a_tag.text.strip()
            full = li.get_text(" ").strip()
            # strip the code off the front of the text
            desc = full[len(code):].strip(" -–:") if full.startswith(code) else full
        else:
            # plain‐text elective or heading
            code = None
            desc = li.get_text(" ").strip()

        courses.append({"code": code, "description": desc})

    # dedupe while preserving order
    seen = set()
    out  = []
    for c in courses:
        key = (c["code"], c["description"])
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out

@router.post("/extract_courses")
async def extracted_courses(req: ExtractRequest):
    """Fetch, parse, upsert into DB, and return the inserted course codes."""
    # 1) Find the program PID
    pid = get_program_pid(req.major)

    # 2) Parse HTML into structured list
    course_list = parse_program_requirements(pid)

    # 3) Upsert each into your `courses` table
    upserted = []
    for item in course_list:
        code = item["code"] or ""
        desc = item["description"]
        raw  = json.dumps(item)  # JSON-stringify for the JSON column

        await database.execute(
            """
            INSERT INTO courses
              (catalog_course_id, pid, title, credits, major, raw_json)
            VALUES
              (:cid, :pid, :title, :credits, :major, :raw)
            ON CONFLICT (catalog_course_id) DO UPDATE
              SET title    = EXCLUDED.title,
                  raw_json = EXCLUDED.raw_json;
            """,
            {
                "cid":     code,
                "pid":     None,
                "title":   desc,
                "credits": 0,
                "major":   req.major,
                "raw":     raw,
            },
        )
        upserted.append(code)

    return {"inserted_courses": upserted}