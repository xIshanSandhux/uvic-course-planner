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
