import os
import json
import re

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai

from database import initialize_database, connect_db

# CONFIGURATION
load_dotenv()

app = FastAPI(
    title="AI Customer Support System",
    description="Customer support ticket management with Gemini AI"
)

initialize_database()

# REQUEST MODELS
class TicketCreate(BaseModel):
    customer: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)


class TicketUpdate(BaseModel):
    status: str
    priority: str

# HOME
@app.get("/")
def home():
    return {
        "message": "Welcome to the AI Customer Support System!"
    }


# VIEW ALL TICKETS
@app.get("/tickets")
def get_tickets():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    connection.close()

    return [dict(ticket) for ticket in tickets]


# CREATE TICKET
@app.post("/tickets")
def create_ticket(ticket: TicketCreate):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tickets (customer, title, description)
        VALUES (?, ?, ?)
    """, (
        ticket.customer.strip(),
        ticket.title.strip(),
        ticket.description.strip()
    ))

    ticket_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "message": "Ticket created successfully!",
        "ticket_id": ticket_id
    }


# UPDATE TICKET
@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, ticket: TicketUpdate):

    allowed_statuses = [
        "Open", "In Progress", "Resolved"
    ]

    allowed_priorities = [
        "Low", "Normal", "High", "Urgent"
    ]

    if ticket.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket status"
        )

    if ticket.priority not in allowed_priorities:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket priority"
        )

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    if cursor.fetchone() is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    cursor.execute("""
        UPDATE tickets
        SET status = ?, priority = ?
        WHERE id = ?
    """, (ticket.status, ticket.priority, ticket_id))

    connection.commit()
    connection.close()

    return {
        "message": "Ticket updated successfully!"
    }


# DELETE TICKET
@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    if cursor.fetchone() is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    cursor.execute(
        "DELETE FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Ticket deleted successfully!"
    }


# AI TICKET ANALYSIS
@app.post("/tickets/{ticket_id}/analyze")
def analyze_ticket(ticket_id: int):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured."
        )

    # Get ticket from database
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    ticket = cursor.fetchone()

    if ticket is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # Prepare the ticket information
    title = ticket["title"]
    description = ticket["description"]

    connection.close()

    # Connect to Gemini
    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an AI assistant for a customer support system.

    Analyze the following customer support ticket.

    Ticket title: {title}

    Ticket description: {description}

    Return ONLY a valid JSON object with these four fields:

    {{
        "category": "One suitable category",
        "priority": "Low, Normal, High, or Urgent",
        "sentiment": "Positive, Neutral, or Negative",
        "suggested_response": "A professional response to the customer"
    }}

    Rules:
    - Choose a relevant category such as Payment,
      Technical Issue, Account, Delivery, or Refund.
    - Select priority based on the seriousness of the issue.
    - Keep the suggested response professional and helpful.
    - Do not claim that a refund or action has already happened.
    - Do not include markdown code fences.
    - Return valid JSON only.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        raw_response = response.text

        if not raw_response:
            raise ValueError("Empty AI response")

        # Removing accidental markdown code fences
        raw_response = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            raw_response.strip(),
            flags=re.IGNORECASE
        )

        result = json.loads(raw_response)

        required_fields = [
            "category",
            "priority",
            "sentiment",
            "suggested_response"
        ]

        if not all(field in result for field in required_fields):
            raise ValueError("Missing AI response fields")

        allowed_priorities = [
            "Low", "Normal", "High", "Urgent"
        ]

        if result["priority"] not in allowed_priorities:
            result["priority"] = "Normal"

    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        
        raise HTTPException(
        status_code=502,
        detail=str(e)
    )

    # Saving AI analysis in SQLite
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tickets
        SET category = ?,
            priority = ?,
            sentiment = ?,
            ai_suggested_response = ?
        WHERE id = ?
    """, (
        result["category"],
        result["priority"],
        result["sentiment"],
        result["suggested_response"],
        ticket_id
    ))

    connection.commit()
    connection.close()

    return {
        "ticket_id": ticket_id,
        "message": "AI analysis completed successfully!",
        "analysis": result
    }
