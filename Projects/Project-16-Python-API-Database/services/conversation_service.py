"""
================================================================================
THIS FILE'S JOB IS TO EXECUTE BUSINESS LOGIC AND COORDINATE PERSISTENCE
================================================================================

1. Why this file exists:
   The "Service Layer" is the heart of an application. API routes should only
   worry about HTTP (status codes, headers, parsing requests). They should NOT
   contain business rules or direct database query logic.
   By keeping business logic here, you can easily reuse it (e.g., from a background
   worker, CLI command, or another API route) without changing anything.

2. What it does:
   - Evaluates the user's banking support inquiry using educational business rules.
   - Generates a relevant support answer based on banking inquiry keywords.
   - Coordinates with SQLAlchemy to persist the conversation to the SQLite database.
   - Retrieves stored conversations for history inspection.

3. Who communicates with it:
   - `api/routes.py` calls functions in this file (`process_and_save_conversation`, `get_all_conversations`).
   - This service communicates with `database/models.py` (to create rows) and `database/connection.py` (via the Session object).

4. What it sends to the next layer:
   - Returns saved database model objects (`Conversation`) back up to the API route.

5. What it receives back:
   - Receives clean, validated data from the API route (`user_message` string, `db` session).

================================================================================
EDUCATIONAL NOTE ON BUSINESS LOGIC:
In a production Generative AI application, this service layer is exactly where you
would call an LLM (such as Google Gemini, OpenAI, or a LangChain/LlamaIndex agent).
For this architecture project, we intentionally use clear, deterministic rule-based
logic so you can master the backend data flow without API latency, billing, or network dependencies.
================================================================================
"""

import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models import Conversation

logger = logging.getLogger("bank_support_service")


def generate_support_response(user_message: str) -> str:
    """
    Simulates intelligent customer support business logic.

    In an AI-enabled system, this function would call an LLM or RAG pipeline.
    Here, it demonstrates educational rule-based keyword routing.
    """
    message_lower = user_message.lower()

    if any(k in message_lower for k in ["fee", "charge", "charged", "cost"]):
        return (
            "Regarding your fee inquiry: Monthly card maintenance fees are assessed on the 1st of each month. "
            "If your account maintains an average daily balance above $500, this fee is automatically waived. "
            "Our support team has logged a fee review request for your account."
        )
    elif any(k in message_lower for k in ["transaction", "payment", "transfer", "pending", "history"]):
        return (
            "Regarding your transaction inquiry: Transactions typically take 1-3 business days to transition "
            "from 'Pending' to 'Posted'. If you notice an unrecognized merchant charge, you can temporarily "
            "freeze your card or dispute the charge within 60 calendar days."
        )
    elif any(k in message_lower for k in ["card", "debit", "credit", "lost", "stolen", "pin"]):
        return (
            "Regarding your card inquiry: For lost or stolen cards, lock your card immediately in mobile banking "
            "under 'Card Controls'. Replacement cards arrive within 3-5 business days at your registered address."
        )
    elif any(k in message_lower for k in ["account", "balance", "routing", "statement", "open"]):
        return (
            "Regarding your account inquiry: You can view your real-time available balance and download past "
            "statements directly through the banking portal. Your routing number is located at the bottom of your checks."
        )
    elif any(k in message_lower for k in ["hello", "hi", "help", "hey"]):
        return (
            "Hello! Welcome to Bank Customer Support. You can ask me questions about your transactions, "
            "card maintenance fees, replacement cards, or account balances."
        )
    else:
        return (
            f"Thank you for contacting Bank Customer Support regarding: '{user_message}'. "
            "Your inquiry has been categorized as General Banking Assistance. An advisor will review your request shortly."
        )


def process_and_save_conversation(db: Session, user_message: str) -> Conversation:
    """
    Main business transaction:
    1. Generates response using application logic.
    2. Instantiates Conversation ORM model.
    3. Persists to SQLite using SQLAlchemy session.
    4. Commits transaction and returns persisted object.
    """
    # Step 1: Execute business logic
    response_text = generate_support_response(user_message)

    # Step 2: Create ORM Model instance
    conversation_record = Conversation(
        user_message=user_message,
        assistant_response=response_text
    )

    # Step 3: Persist via SQLAlchemy
    try:
        db.add(conversation_record)
        db.commit()
        db.refresh(conversation_record)
        return conversation_record
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error(f"Database error while saving conversation: {exc}")
        raise RuntimeError(f"Database persistence failure: {str(exc)}") from exc


def get_all_conversations(db: Session, limit: int = 50) -> List[Conversation]:
    """
    Retrieves stored conversations ordered by most recent first.
    Allows frontend to inspect persistent database state through the API.
    """
    try:
        return (
            db.query(Conversation)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as exc:
        logger.error(f"Database error while reading conversations: {exc}")
        raise RuntimeError(f"Failed to query conversations: {str(exc)}") from exc
