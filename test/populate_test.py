# populate_test.py
import os, asyncio, json
from databases import Database
from dotenv import load_dotenv

load_dotenv()
DB = Database(os.getenv("DATABASE_URL"))

async def run():
    await DB.connect()

    raw_data = {"foo": "bar"}
    raw_str  = json.dumps(raw_data)

    # Upsert on catalog_course_id
    await DB.execute(
        """
        INSERT INTO courses
          (catalog_course_id, pid, title, credits, major, raw_json)
        VALUES
          (:cid, :pid, :title, :credits, :major, :raw_json)
        ON CONFLICT (catalog_course_id) DO UPDATE
          SET pid      = EXCLUDED.pid,
              title    = EXCLUDED.title,
              credits  = EXCLUDED.credits,
              major    = EXCLUDED.major,
              raw_json = EXCLUDED.raw_json;
        """,
        {
            "cid":      "TEST100",
            "pid":      "P100",
            "title":    "Updated Dummy Course",
            "credits":  4,
            "major":    "TEST_MAJ",
            "raw_json": raw_str,
        }
    )

    row = await DB.fetch_one(
        "SELECT * FROM courses WHERE catalog_course_id = 'TEST100';"
    )
    print("Upserted row:", row)

    await DB.disconnect()

if __name__ == "__main__":
    asyncio.run(run())
