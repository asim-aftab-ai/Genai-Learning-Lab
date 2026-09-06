"""
================================================================================
THIS FILE'S JOB IS TO EXPOSE HTTP API ROUTES (COMMUNICATION DISPATCHER)
================================================================================

1. Why this file exists:
   An API route file acts as the translator between the outside world (HTTP requests)
   and the application's internal functions. It inspects URL paths, HTTP verbs
   (GET, POST), and request bodies, then routes them to the correct business service.

2. What it does:
   - Exposes `POST /conversations`: Receives a customer support question, triggers
     the service layer, and returns the newly saved conversation.
   - Exposes `GET /conversations`: Retrieves all previous customer support conversations
     from the database to display in the Streamlit frontend.
   - Exposes `GET /health`: A lightweight status check to verify the API is running.
   - Converts Python exceptions into proper HTTP status codes (201, 400, 500).

3. Who communicates with it:
   - Streamlit (frontend) calls these endpoints over HTTP using requests.
   - `api/main.py` mounts this router on the FastAPI application.

4. What it sends to the next layer:
   - Extracts validated data from Pydantic schemas and passes it to `services/conversation_service.py`.

5. What it receives back:
   - Receives database records from `conversation_service.py` and lets FastAPI/Pydantic
     serialize them into clean JSON responses for the frontend.
================================================================================
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.conversation_schema import ConversationCreateRequest, ConversationResponse
from services.conversation_service import process_and_save_conversation, get_all_conversations

# APIRouter groups endpoints cleanly. It keeps main.py small and uncluttered.
router = APIRouter(prefix="/api", tags=["Bank Support"])


@router.get("/health", summary="API Health Check")
def health_check():
    """
    Simple endpoint used by Streamlit or monitoring tools to verify
    the FastAPI backend service is alive and reachable.
    """
    return {
        "status": "healthy",
        "service": "Bank Customer Support API",
        "version": "1.0.0"
    }


@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a customer support inquiry"
)
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Primary Request Flow:
    1. Streamlit sends JSON: {"user_message": "..."}
    2. FastAPI validates payload against ConversationCreateRequest schema.
    3. Route calls the Service Layer (conversation_service).
    4. Service executes business logic and saves to SQLite via SQLAlchemy.
    5. Route returns ConversationResponse (serialized back to JSON).
    """
    try:
        saved_record = process_and_save_conversation(db=db, user_message=request.user_message)
        return saved_record
    except ValueError as ve:
        # Client validation or logic rejection (Bad Request)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        # Database or server-side failure (Internal Server Error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(exc)}"
        )


@router.get(
    "/conversations",
    response_model=List[ConversationResponse],
    summary="List recent customer support conversations"
)
def list_conversations(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Retrieval Flow for Database Visibility:
    1. Streamlit requests conversation history to prove persistence.
    2. Route calls conversation_service.get_all_conversations.
    3. SQLAlchemy reads persisted records from SQLite.
    4. Route serializes list of records into JSON and returns to Streamlit.
    """
    try:
        records = get_all_conversations(db=db, limit=limit)
        return records
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to retrieve conversations: {str(exc)}"
        )
