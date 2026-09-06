# Project 16: Python API & Database Architecture (Bank Customer Support System)

> **Core Learning Goal:** Master the fundamental system design concept:  
> **`Request → API → Application Logic → Database → Response`**

---

## 1. What the Project Does

This project is an educational **Bank Customer Support System**. It allows a customer to submit banking support inquiries (e.g., questions regarding card maintenance fees, pending transactions, or replacement cards) through a modern Streamlit web frontend.

The system processes the inquiry across a multi-tier backend built with FastAPI, applies business logic in a dedicated service layer, persists the conversation record into a SQLite database using SQLAlchemy ORM, and returns the response back to the user.

---

## 2. Why the Project Exists

In early programming tutorials, it is common to build "monolithic" scripts where the frontend code, business logic, SQL queries, and database drivers all live in a single `.py` file.

While simple, monolithic scripts do not reflect how real-world software, AI microservices, or production systems are architected. This project exists to teach **clean separation of concerns**:
- Why APIs act as the essential bridge between user interfaces and databases.
- How data flows across distinct layers of an application.
- Why security, scalability, and maintainability demand this separation.

---

## 3. High-Level Architecture

The application strictly follows this unidirectional request/response lifecycle:

```text
                 USER
                   ↓
             STREAMLIT UI
                   ↓ [HTTP POST JSON]
              FASTAPI (main.py)
                   ↓
              API ROUTE (routes.py)
                   ↓ [Python Function Call]
           SERVICE LAYER (conversation_service.py)
                   ↓ [ORM Entity Creation]
              SQLALCHEMY (Session & Models)
                   ↓ [SQL INSERT / SELECT]
              SQLITE DB (bank_support.db)
                   ↓ [Persisted Record]
              SQLALCHEMY
                   ↓ [Model Object]
           SERVICE LAYER
                   ↓ [Entity Return]
             API ROUTE
                   ↓ [Pydantic Response Serialization]
              FASTAPI
                   ↓ [HTTP 201 Created JSON]
             STREAMLIT UI
                   ↓
                 USER
```

---

## 4. Folder Structure & Roles

```text
Project-16-Python-API-Database/
│
├── frontend/                     # Tier 1: Client / Presentation
│   └── streamlit_app.py          # Interactive web UI and API caller
│
├── api/                          # Tier 2: HTTP Transport & Routing
│   ├── __init__.py               # Exposes API router
│   ├── main.py                   # FastAPI server entrypoint & lifecycle
│   └── routes.py                 # HTTP endpoints & request dispatching
│
├── services/                     # Tier 3: Business Logic
│   ├── __init__.py               # Exposes service functions
│   └── conversation_service.py   # Decision logic & DB coordination
│
├── database/                     # Tier 4: Data Persistence Layer
│   ├── __init__.py               # Exposes DB engines and models
│   ├── connection.py             # SQLite engine, sessions, init_db()
│   └── models.py                 # SQLAlchemy ORM table definitions
│
├── schemas/                      # Tier 5: Data Validation Contracts
│   ├── __init__.py               # Exposes Pydantic schemas
│   └── conversation_schema.py   # Request and Response schemas
│
├── README.md                     # Comprehensive educational documentation
└── __init__.py                   # Project root package marker
```

---

## 5. File Responsibilities Breakdown

Every file in this project has **exactly one single responsibility**:

| File | Primary Responsibility | Communicates With |
| :--- | :--- | :--- |
| **`frontend/streamlit_app.py`** | Renders UI, displays live request flow, and queries API. Never touches the database directly. | Human User, FastAPI over HTTP |
| **`api/main.py`** | Initializes the FastAPI app, manages startup/shutdown lifespan, and mounts routes. | Uvicorn ASGI server, `api/routes.py` |
| **`api/routes.py`** | Validates incoming HTTP payloads and dispatches work to the service layer. | `frontend/streamlit_app.py`, `services/conversation_service.py` |
| **`services/conversation_service.py`** | Executes business logic (rules standing in for AI agents) and coordinates database persistence. | `api/routes.py`, `database/models.py`, `database/connection.py` |
| **`database/connection.py`** | Configures the SQLite database engine, session factory, and table creation. | `api/main.py`, `database/models.py`, `services/conversation_service.py` |
| **`database/models.py`** | Defines the SQLAlchemy ORM `Conversation` table schema. | `database/connection.py`, `services/conversation_service.py` |
| **`schemas/conversation_schema.py`** | Defines Pydantic validation models for HTTP request payloads and responses. | `api/routes.py` |

---

## 6. The Complete Request / Response Journey

When a user clicks **"Send to Bank Support API"** in Streamlit, here is the exact journey of that request:

1. **User Action:** The user types `"Why was I charged a card fee?"` and submits the form.
2. **HTTP Transmission:** `streamlit_app.py` packages the message into a JSON payload (`{"user_message": "..."}`) and sends an HTTP `POST` request to `http://127.0.0.1:8000/api/conversations`.
3. **API Ingestion:** FastAPI receives the request and parses the body against `ConversationCreateRequest`. If the message is empty or missing, FastAPI immediately rejects it with an HTTP 400 or 422 error.
4. **Route Dispatch:** `api/routes.py` receives the validated request and passes the input string to `conversation_service.process_and_save_conversation()`.
5. **Business Logic:** `services/conversation_service.py` analyzes the inquiry keywords (e.g. "fee") and generates a structured bank support advisory.
6. **ORM Mapping:** The service instantiates a `Conversation` model (`database/models.py`) with the user's inquiry and the generated response.
7. **Database Persistence:** SQLAlchemy generates and executes an `INSERT INTO conversations ...` SQL statement against the local `bank_support.db` SQLite database file.
8. **Transaction Commit:** The database commits the new row, generates an auto-incremented primary key `id`, and returns the refreshed entity to the service.
9. **Route Serialization:** The service passes the persisted model back to `api/routes.py`. Pydantic's `ConversationResponse` schema serializes the model into JSON.
10. **HTTP Response:** FastAPI sends an `HTTP 201 Created` response back across the network to Streamlit.
11. **UI Presentation:** Streamlit parses the JSON, renders the conversation response card, updates the database ID badge, and animates the live step trace.

---

## 7. Deep-Dive Conceptual Questions

### Why does Streamlit communicate with FastAPI instead of SQLite directly?
1. **Security:** Frontends run on user devices or browsers. If a frontend accessed a database directly, database connection credentials (passwords, hostnames) would have to be distributed publicly, creating a severe security vulnerability.
2. **Centralized Business Rules:** If banking rules change (e.g., fee waiver requirements), updating them in the API service immediately updates all clients (web, mobile, third-party partners) without requiring client updates.
3. **Connection Pooling & Scalability:** Direct database connections from hundreds or thousands of frontends will quickly exhaust database socket limits and crash the database. An API controls and pools connections safely.

### Why are Database Models and API Schemas separate concepts?
- **Database Models (`database/models.py`):**
  - Define how data is physically stored on disk (columns, data types, indexes, foreign keys, relationships).
  - Tied to the database engine via SQLAlchemy.
- **API Schemas (`schemas/conversation_schema.py`):**
  - Define how data moves over the network (HTTP JSON payloads, input validation rules, required fields).
  - Protects internal details (e.g., internal flags, database primary key mechanics, or sensitive credentials should never be directly mapped from raw tables into public APIs).

### How does this small project relate to real production AI systems?
In a production Generative AI application (such as an AI Agent or RAG system):
- `conversation_service.py` is where you would call an LLM (such as **Google Gemini** or **OpenAI**) or an agent workflow.
- Everything else—FastAPI, routes, SQLAlchemy, SQLite/PostgreSQL, Pydantic schemas, and Streamlit—remains **exactly the same**. Mastering this skeleton gives you the real-world foundation for any AI product.

---

## 8. How to Run the Project

This project consists of two independent services running concurrently:
1. **FastAPI Backend Server** (Port 8000)
2. **Streamlit Frontend Web App** (Port 8501)

Always use the existing root-level `.venv` virtual environment.

### Terminal 1: Start the FastAPI Backend
Open a terminal in the root workspace directory (`Genai-Learning-Lab/`):

```powershell
# 1. Activate root virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 2. Navigate to the project directory
cd Projects\Project-16-Python-API-Database

# 3. Start the FastAPI server with auto-reload
python -m uvicorn api.main:app --reload --port 8000
```
> The API server will start at: `http://127.0.0.1:8000`  
> Interactive Swagger API Documentation: `http://127.0.0.1:8000/docs`

---

### Terminal 2: Start the Streamlit Frontend
Open a second terminal in the root workspace directory:

```powershell
# 1. Activate root virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 2. Navigate to the project directory
cd Projects\Project-16-Python-API-Database

# 3. Launch Streamlit
python -m streamlit run frontend\streamlit_app.py
```
> The Streamlit application will open in your browser at: `http://localhost:8501`

---

## 9. Testing & Verifying Persistence
1. With both services running, navigate to `http://localhost:8501`.
2. Observe the sidebar: **Architecture Monitor** will display `Backend Online`.
3. Select or type a question (e.g., *"Why was I charged a card fee?"*) and click **"Send to Bank Support API"**.
4. Observe the **Visible Request/Response Flow** animating each layer of the architecture.
5. Notice the **Database Assigned Record ID** (e.g. `#1`).
6. Click the **"Database Records (Via API)"** tab to view your conversation permanently stored in SQLite, fetched strictly via `GET /api/conversations`.
