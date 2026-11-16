# AI-Powered Customer Support Ticket System

A backend application built with **Python, FastAPI, and SQLite** to manage customer support tickets, with an AI integration using Google's Gemini API currently under development.

## Project Overview

The AI-Powered Customer Support Ticket System is designed to simplify customer support operations by providing a centralized platform for creating, managing, tracking, and analyzing customer support tickets.

The project combines backend development with AI-powered automation to explore how Large Language Models (LLMs) can improve customer support workflows.

## Features

### Ticket Management
- Create new customer support tickets.
- View all submitted tickets.
- Update ticket status and priority.
- Delete existing tickets.
- Automatically assign unique ticket IDs.

### Database Management
- SQLite database integration.
- Persistent storage of ticket information.
- Automatic database initialization.
- Additional fields for AI-generated ticket analysis.

### AI Integration (In Progress)
- Automatic ticket categorization.
- AI-based priority suggestions.
- Customer sentiment analysis.
- AI-generated suggested responses.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLite | Database management |
| Google Gemini API | AI-powered ticket analysis |
| Pydantic | Request data validation |
| Uvicorn | ASGI server |

## Project Structure

```text
AI-Customer-Support-System/
│
├── main.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md
```

The SQLite database and environment configuration are generated or maintained locally and are excluded from version control.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd AI-Customer-Support-System
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/api-keys).

**Important:** Never upload your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
python -m uvicorn main:app --reload
```

### 6. Access the API documentation

Open the following URL in your browser:

```text
http://127.0.0.1:8000/docs
```

FastAPI provides interactive API documentation through Swagger UI.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome endpoint |
| GET | `/tickets` | Retrieve all tickets |
| POST | `/tickets` | Create a new ticket |
| PUT | `/tickets/{ticket_id}` | Update ticket status and priority |
| DELETE | `/tickets/{ticket_id}` | Delete a ticket |
| POST | `/tickets/{ticket_id}/analyze` | Analyze a ticket using Gemini AI |

## Future Improvements

- Implement customer and support agent authentication.
- Introduce role-based access control.
- Build a frontend dashboard using Streamlit.
- Improve AI error handling and response reliability.
- Add ticket search, filtering, and reporting.
- Implement automated ticket assignment.

## Learning Outcomes

Through this project, I am exploring:

- Building REST APIs using FastAPI.
- Database integration using SQLite.
- CRUD operations and data validation.
- Integrating external AI APIs.
- Environment variable management and API security.
- Backend application architecture.

## Project Status

**Currently in development.**

The core ticket management API and SQLite database integration are implemented. Gemini AI integration is under development, with frontend development and authentication planned for future versions.

---

**Developed as a personal portfolio project.**
