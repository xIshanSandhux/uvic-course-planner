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
- **Request Body**: 
  ```json
  {
    "major": "Software Engineering"
  }
  ```
  **Type**: `ExtractRequest` (Pydantic model with `major: str`)
- **Response**: 
  ```json
  [
    "CSC 110: Fundamentals of Programming I",
    "CSC 115: Fundamentals of Programming II", 
    "MATH 100: Calculus I"
  ]
  ```
  **Type**: `List[str]` (Array of course strings)
- **Functionality**: 
  - Checks if major exists in database
  - If exists: returns stored course list
  - If not: fetches from UVic API, stores in background, returns immediate list
  - Course format: "CODE: Description"

#### `/courses_completed` (POST)
- **Purpose**: Set courses completed by the user
- **Request Body**: 
  ```json
  {
    "courses": [
      "CSC 110: Fundamentals of Programming I",
      "MATH 100: Calculus I"
    ]
  }
  ```
  **Type**: `ExtractRequest` (Pydantic model with `courses: List[str]`)
- **Response**: 
  ```json
  {
    "message": "Courses completed posted successfully"
  }
  ```
  **Type**: `Dict[str, str]` (Object with message field)
- **Error Response**: `HTTPException` with status code 500 and error detail
- **Functionality**: 
  - Stores user's completed courses in session memory
  - Converts course list to comma-separated string for storage
  - Validates course data before storing

#### `/courses_completed` (GET)
- **Purpose**: Get courses completed by the user
- **Request Body**: None
- **Response**: 
  ```
  "CSC 110: Fundamentals of Programming I, MATH 100: Calculus I"
  ```
  **Type**: `str` (Comma-separated string)
- **Error Response**: `Dict[str, str]` with error message
- **Functionality**: 
  - Retrieves completed courses from session memory
  - Returns courses as comma-separated string
  - Handles empty course lists gracefully

#### `/course_list` (POST)
- **Purpose**: Set the course list for a major
- **Request Body**: 
  ```json
  {
    "courses": [
      "CSC 110: Fundamentals of Programming I",
      "CSC 115: Fundamentals of Programming II",
      "MATH 100: Calculus I"
    ]
  }
  ```
  **Type**: `ExtractRequest` (Pydantic model with `courses: List[str]`)
- **Response**: 
  ```json
  {
    "message": "Course list posted successfully"
  }
  ```
  **Type**: `Dict[str, str]` (Object with message field)
- **Error Response**: `HTTPException` with status code 500 and error detail
- **Functionality**: 
  - Stores full course list for selected major in session
  - Converts array to comma-separated string for consistency
  - Used as reference for filtering available courses

#### `/course_list` (GET)
- **Purpose**: Get the course list for a major
- **Request Body**: None
- **Response**: 
  ```
  "CSC 110: Fundamentals of Programming I, CSC 115: Fundamentals of Programming II, MATH 100: Calculus I"
  ```
  **Type**: `str` (Comma-separated string)
- **Error Response**: `Dict[str, str]` with error message
- **Functionality**: 
  - Retrieves stored course list from session memory
  - Returns all courses for the selected major
  - Provides reference for course selection and filtering

#### `/courses_not_completed` (GET)
- **Purpose**: Get courses not completed by the user that are offered in the current term
- **Request Body**: None
- **Response**: 
  ```json
  [
    "CSC 115: Fundamentals of Programming II",
    "MATH 101: Calculus II"
  ]
  ```
  **Type**: `List[str]` (Array of course strings)
- **Functionality**: 
  - Returns courses from session that haven't been completed
  - Filters based on availability in current term
  - Checks Summer availability in database

#### `/courses_not_completed` (POST)
- **Purpose**: Process and filter courses not completed
- **Request Body**: None (uses session data from previous endpoints)
- **Response**: 
  ```json
  {
    "message": "Courses not completed posted successfully"
  }
  ```
  **Type**: `Dict[str, str]` (Object with message field)
- **Functionality**: 
  - Compares completed courses with major requirements
  - Filters courses available in current term (Summer)
  - Updates session with filtered course list

#### `/pre_req_check` (POST)
- **Purpose**: Check prerequisites for courses not completed
- **Request Body**: None (uses session data)
- **Response**: 
  ```json
  {
    "message": "Pre-req check posted successfully"
  }
  ```
  **Type**: `Dict[str, str]` (Object with message field)
- **Functionality**: 
  - Analyzes prerequisites for each course not completed
  - Checks if user has completed required prerequisites
  - Updates session with courses user can take

### AI Chat Endpoints

#### `/cohere/chat` (POST)
- **Purpose**: AI chat using Cohere's Command-R model
- **Request Body**: 
  ```json
  {
    "messages": [
      {"role": "user", "content": "What courses should I take next semester?"},
      {"role": "assistant", "content": "Based on your completed courses..."}
    ]
  }
  ```
  **Type**: `ChatRequest` (Pydantic model with `messages: List[ChatMessage]`)
- **Response**: 
  ```json
  {
    "success": true, 
    "content": [{"text": "Based on your academic progress..."}]
  }
  ```
  **Type**: `Dict[str, Union[bool, List[Dict[str, str]]]]` (Object with success flag and content array)
- **Functionality**: 
  - Maintains chat history and conversation context
  - Processes user queries with course planning context
  - Returns AI-generated responses for academic guidance

#### `/google/chat` (POST)
- **Purpose**: AI chat using Google's Gemma-3-27b-it model
- **Request Body**: 
  ```json
  {
    "messages": [
      {"role": "user", "content": "What courses should I take next semester?"},
      {"role": "assistant", "content": "Based on your completed courses..."}
    ]
  }
  ```
  **Type**: `ChatRequest` (Pydantic model with `messages: List[ChatMessage]`)
- **Response**: 
  ```json
  {
    "success": true, 
    "content": [{"text": "Based on your academic progress..."}]
  }
  ```
  **Type**: `Dict[str, Union[bool, List[Dict[str, str]]]]` (Object with success flag and content array)
- **Functionality**: 
  - Provides alternative AI chat using Google's model
  - Maintains conversation context and history
  - Returns plain text responses for course planning assistance

## Session Management

The backend uses a `SessionManager` class to maintain state between requests:

- **courses_completed**: List of courses user has completed
- **courses_list**: Full course list for the selected major
- **courses_not_completed**: Filtered list of available courses
- **pre_req_comp_courses**: Courses user can take based on prerequisites

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
COHERE_API_KEY=your_cohere_api_key
GOOGLE_API_KEY=your_google_api_key
```

## CORS Configuration

The API is configured with CORS middleware to allow cross-origin requests from the frontend application. Currently set to allow all origins (`"*"`) for development purposes.

```
