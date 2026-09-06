"""
================================================================================
THIS FILE'S JOB IS TO DEFINE API REQUEST AND RESPONSE SCHEMAS (DATA CONTRACTS)
================================================================================

1. Why this file exists:
   Clients (like Streamlit, web browsers, or mobile apps) send JSON over HTTP.
   Before our application logic touches this data, we must validate that:
   - Required fields are present.
   - Data types are correct.
   - Inputs are clean and not empty.
   Similarly, when sending data back to the client, we must format and serialize it.
   Pydantic schemas define the strict data contract for the API.

2. What it does:
   - Defines `ConversationCreateRequest`: The schema for incoming client requests.
   - Defines `ConversationResponse`: The schema for outgoing server responses.

3. Who communicates with it:
   - `api/routes.py` uses `ConversationCreateRequest` to validate incoming POST bodies.
   - `api/routes.py` uses `ConversationResponse` as the response_model to format output.

4. What it sends to the next layer:
   - Validated Python data objects to the API route and service functions.

5. What it receives back:
   - Validated data objects converted into JSON for the HTTP client (Streamlit).

================================================================================
CRITICAL CONCEPT: Why are API Schemas separate from Database Models?
================================================================================
1. Database Models (`database/models.py`):
   - Focus on STORAGE (relational structure, primary keys, foreign keys, table columns).
   - Tied to SQLite / database engine via SQLAlchemy.

2. API Schemas (`schemas/conversation_schema.py`):
   - Focus on COMMUNICATION (network payloads, API contracts, input validation).
   - Protects internal database details (e.g., you would never expose a user's hashed password
     or internal database flags in an API schema, even though they exist in a database model).
   - Allows request and response formats to differ from table storage.
================================================================================
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ConversationCreateRequest(BaseModel):
    """
    Schema representing the incoming HTTP request payload from Streamlit.

    Expected JSON body:
    {
        "user_message": "Why was I charged a card fee?"
    }
    """
    user_message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The customer support inquiry or question."
    )

    @field_validator("user_message")
    @classmethod
    def message_must_not_be_whitespace(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Customer support question cannot be empty or only whitespace.")
        return cleaned


class ConversationResponse(BaseModel):
    """
    Schema representing the outgoing HTTP response sent back to Streamlit.

    Output JSON payload:
    {
        "id": 1,
        "user_message": "Why was I charged a card fee?",
        "assistant_response": "...",
        "created_at": "2026-09-06T15:00:00Z"
    }
    """
    id: int
    user_message: str
    assistant_response: str
    created_at: datetime

    # ConfigDict(from_attributes=True) allows Pydantic to read data directly
    # from SQLAlchemy ORM model instances (e.g., model.user_message)
    model_config = ConfigDict(from_attributes=True)
