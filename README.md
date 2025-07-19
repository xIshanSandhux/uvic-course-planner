# First create the virtual environment (you've already done this)

python -m venv venv

# Then activate it using this command for Windows PowerShell

.\venv\Scripts\Activate

pip install -r requirement.txt

# To Run:

# Backend:

uvicorn backend.main:app --reload

# Frontend:

streamlit run frontend/landing_page.py

# to access database:

psql -U postgres -h localhost -p 5432

# connect to course_planner db using course_planner_user user account

\c course_planner course_planner_user

# update:

## For backend:

venv\Scripts\activate
uvicorn backend.main:app --reload

## For frontend:

cd frontend
venv\Scripts\activate
npm run dev

# Make sure you have 2 .env files

/your-project/
├── .env ← Backend secrets (used by FastAPI)
├── backend/
│ └── main.py
├── react-frontend/
│ ├── .env ← Frontend variables (e.g., VITE_COHERE_API_KEY)
│ └── vite.config.js
