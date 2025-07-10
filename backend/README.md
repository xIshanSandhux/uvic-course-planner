# Backend API

This is the backend, built with FastAPI (Python).

## Tech Stack

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs with Python
- **Uvicorn** - ASGI server for running FastAPI applications
- **Pydantic** - Data validation and settings management

### Database
- **PostgreSQL** - Primary database for storing course and user data
- **SQLAlchemy** - SQL toolkit and ORM
- **Databases** - Async database support for FastAPI
- **asyncpg** - Async PostgreSQL driver

### AI/LLM Integration
- **Cohere** - AI chat functionality with Command-R model
- **Google Gemini** - Alternative AI chat with Gemma-3-27b-it model

### Web Scraping & Automation
- **Playwright** - Browser automation for course availability checking
- **BeautifulSoup4** - HTML parsing for course data extraction
- **Requests** - HTTP library for API calls

### Development & Deployment
- **Python 3.11** - Runtime environment
- **Docker** - Containerization
- **python-dotenv** - Environment variable management

## Architecture

The backend follows a modular architecture with the following structure:

```
backend/
├── main.py                 # FastAPI application entry point
├── db.py                   # Database models and connection
├── api/
│   ├── courses/           # Course-related endpoints
│   │   ├── extract_courses.py
│   │   └── course_complete.py
│   └── llm/              # AI chat endpoints
│       ├── cohere_chat.py
│       └── google_gemma_chat.py
├── requirements.txt       # Python dependencies
└── Dockerfile           # Container configuration
```

## Database Schema

### Tables

1. **courses** - Stores course information with prerequisites
   - `id` (Primary Key)
   - `catalog_course_id` (Unique, indexed)
   - `pid` (Indexed)
   - `title`
   - `credits`
   - `major`
   - `prerequisites` (JSON)
   - `raw_json` (JSON)

2. **courses_main** - Main course data table
   - `id` (Primary Key)
   - `pid` (Unique, indexed)
   - `course_code` (Indexed)
   - `course_name`
   - `course_description`
   - `prerequisites` (JSON)
   - `credits`
   - `Summer` (Boolean)

3. **majors** - Stores major/program information
   - `id` (Primary Key)
   - `major` (Unique, indexed)
   - `major_pid` (Indexed)
   - `courses` (JSON)

## API Endpoints

### Course Management

#### `/extract_courses` (POST)
- **Purpose**: Extract and store course data for a specific major
- **Request Body**: `{"major": "string"}`

#### `/courses_completed` (POST)
- **Purpose**: Set courses completed by the user
- **Request Body**: `{"courses": ["string"]}`
- **Response**: `{"message": "Courses completed posted successfully"}`

#### `/courses_completed` (GET)
- **Purpose**: Get courses completed by the user
- **Response**: Comma-separated string of completed courses

#### `/course_list` (POST)
- **Purpose**: Set the course list for a major
- **Request Body**: `{"courses": ["string"]}`
- **Response**: `{"message": "Course list posted successfully"}`

#### `/course_list` (GET)
- **Purpose**: Get the course list for a major
- **Response**: Comma-separated string of courses

#### `/courses_not_completed` (GET)
- **Purpose**: Get courses not completed by the user that are offered in the current term
- **Functionality**: 
  - Compares completed courses with major requirements
  - Checks course availability using Playwright automation
  - Returns filtered list of available courses

#### `/courses_not_completed` (POST)
- **Purpose**: Process and filter courses not completed
- **Functionality**: 
  - Fetches all courses from database
  - Checks availability for Summer 2025 term
  - Updates database with availability status

### AI Chat Endpoints

#### `/cohere/chat` (POST)
- **Purpose**: AI chat using Cohere's Command-R model
- **Request Body**: `{"messages": [{"role": "user|assistant|system", "content": "string"}]}`
- **Response**: `{"success": true, "content": [{"text": "response"}]}`
- **Features**:
  - Maintains chat history
  - Supports system prompts
  - Temperature set to 0.3 for consistent responses

#### `/google/chat` (POST)
- **Purpose**: AI chat using Google's Gemma-3-27b-it model
- **Request Body**: `{"messages": [{"role": "user|assistant|system", "content": "string"}]}`
- **Response**: `{"success": true, "content": [{"text": "response"}]}`
- **Features**:
  - Alternative to Cohere chat
  - Plain text responses only
  - Maintains conversation context

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
COHERE_API_KEY=your_cohere_api_key
GOOGLE_API_KEY=your_google_api_key
```

## CORS Configuration

The API is configured with CORS middleware to allow cross-origin requests from the frontend application. Currently set to allow all origins (`"*"`) for development purposes.
