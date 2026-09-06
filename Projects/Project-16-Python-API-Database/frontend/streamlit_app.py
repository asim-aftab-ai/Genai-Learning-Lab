"""
================================================================================
THIS FILE'S JOB IS TO SERVE AS THE STREAMLIT USER INTERFACE (CLIENT LAYER)
================================================================================

1. Why this file exists:
   Users do not interact with raw JSON APIs or database tables. They need an
   interactive graphical user interface (UI). Streamlit acts as the presentation
   layer for this application.

2. What it does:
   - Renders a clean bank customer support portal in the browser.
   - Collects customer support questions from the user.
   - Sends questions to the FastAPI backend over HTTP using the requests library.
   - Visually reveals the Request/Response Flow step-by-step for educational transparency.
   - Fetches and displays recent conversations from the database VIA THE API to prove persistence.

3. Who communicates with it:
   - The human end-user enters questions into this interface.
   - This script communicates over HTTP with api/routes.py (FastAPI).

4. What it sends to the next layer:
   - HTTP POST to http://127.0.0.1:8000/api/conversations with JSON payload.
   - HTTP GET to http://127.0.0.1:8000/api/conversations for history.

5. What it receives back:
   - HTTP JSON responses containing the assistant's answer and database record metadata.

================================================================================
CRITICAL ARCHITECTURAL RULE:
This frontend script NEVER imports SQLAlchemy, NEVER touches database/, and NEVER
reads bank_support.db directly. All data access must pass through FastAPI!
================================================================================
"""

import time
import requests
import streamlit as st

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Bank Support Assistant | System Architecture Lab",
    layout="wide"
)

# Custom styling for professional aesthetic and educational highlights
st.markdown("""
<style>
    .reportview-container {
        background: #f8fafc;
    }
    .flow-card {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 1.25rem;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 1rem;
        font-family: monospace;
    }
    .flow-step {
        margin-bottom: 0.4rem;
        color: #94a3b8;
    }
    .flow-step-active {
        color: #38bdf8;
        font-weight: bold;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# Helper Functions: HTTP API Communication
# ------------------------------------------------------------------------------
def check_api_health():
    """Checks if the FastAPI backend is running and reachable."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=2.0)
        return response.status_code == 200, response.json() if response.status_code == 200 else {}
    except requests.exceptions.RequestException:
        return False, {}


def send_support_question(question: str):
    """Sends user question to FastAPI backend via HTTP POST."""
    url = f"{API_BASE_URL}/api/conversations"
    payload = {"user_message": question}
    response = requests.post(url, json=payload, timeout=5.0)
    return response


def fetch_recent_conversations(limit: int = 10):
    """Fetches stored conversations through the FastAPI backend via HTTP GET."""
    url = f"{API_BASE_URL}/api/conversations?limit={limit}"
    response = requests.get(url, timeout=5.0)
    return response


# ------------------------------------------------------------------------------
# Header & Architecture Banner
# ------------------------------------------------------------------------------
st.title("Apex Community Bank — Customer Support")
st.caption("Project 16: Educational System Design Demo — Request → API → Service → Database → Response")

# Check backend status immediately
api_healthy, health_data = check_api_health()

with st.sidebar:
    st.header("Architecture Monitor")
    if api_healthy:
        st.success(f"Backend Online: {API_BASE_URL}")
        st.caption(f"Service: `{health_data.get('service', 'FastAPI')}`")
    else:
        st.error("Backend Offline")
        st.warning(
            "FastAPI is not reachable. Please start the backend in a separate terminal:\n\n"
            "```powershell\n"
            ".\\.venv\\Scripts\\python.exe -m uvicorn api.main:app --reload\n"
            "```"
        )

    st.markdown("---")
    st.subheader("Request Lifecycle")
    st.code(
        """User
  ↓
Streamlit (Frontend)
  ↓ [HTTP POST]
FastAPI (API Entrypoint)
  ↓
API Route (/conversations)
  ↓
Service Layer (Logic)
  ↓
SQLAlchemy (ORM)
  ↓
SQLite (Database)
  ↓
Service Layer
  ↓
API Route (Serialization)
  ↓ [HTTP 201 Response]
Streamlit UI
  ↓
User""",
        language="text"
    )
    st.info("**Key Rule:** Streamlit NEVER accesses SQLite directly. Everything flows through the API!")


# ------------------------------------------------------------------------------
# Main Application Tabs
# ------------------------------------------------------------------------------
tab_ask, tab_history, tab_concepts = st.tabs([
    "Ask Support & View Live Flow",
    "Database Records (Via API)",
    "Architecture & Concepts"
])

# ------------------------------------------------------------------------------
# TAB 1: Ask Support & Live Request Flow
# ------------------------------------------------------------------------------
with tab_ask:
    st.markdown("### Enter a Customer Support Inquiry")
    st.write("Submit a question to see how the request travels across all 5 architectural tiers:")

    # Quick sample prompt buttons
    st.write("**Or try one of these common bank questions:**")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    sample_choice = None
    if col_q1.button("Why was I charged a card fee?"):
        sample_choice = "Why was I charged a card fee?"
    if col_q2.button("Help with recent transaction"):
        sample_choice = "I want help with my recent transaction."
    if col_q3.button("Lost my debit card"):
        sample_choice = "I lost my debit card, what should I do?"
    if col_q4.button("Check my account balance"):
        sample_choice = "How do I check my account balance?"

    # Input form
    with st.form(key="support_form"):
        default_val = sample_choice if sample_choice else ""
        user_question = st.text_input(
            "Your Message / Inquiry:",
            value=default_val,
            placeholder="e.g., Why was I charged a monthly service fee?"
        )
        submit_button = st.form_submit_button("Send to Bank Support API", use_container_width=True)

    if submit_button:
        # Input validation on frontend
        if not user_question or not user_question.strip():
            st.error("Validation Error: Please enter a non-empty question.")
        elif not api_healthy:
            st.error("Connection Error: The FastAPI backend is not running. Please start it on port 8000 first.")
        else:
            # ------------------------------------------------------------------
            # VISIBLE REQUEST/RESPONSE FLOW (Educational Transparency)
            # ------------------------------------------------------------------
            flow_placeholder = st.empty()

            steps = [
                "1. User entered question in Streamlit UI",
                "2. Streamlit packaged JSON & sent HTTP POST /api/conversations",
                "3. FastAPI backend received HTTP request",
                "4. API Route (api/routes.py) validated schema & invoked Service Layer",
                "5. Service Layer (services/conversation_service.py) processed banking rules",
                "6. Service Layer saved conversation to SQLite database via SQLAlchemy ORM",
                "7. FastAPI serialized ConversationResponse JSON (HTTP 201 Created)",
                "8. Streamlit frontend received HTTP response",
                "9. Response displayed to user"
            ]

            # Educational animation/progress display
            with flow_placeholder.container():
                with st.expander("**Visible Request/Response Flow (Click to collapse)**", expanded=True):
                    flow_box = st.empty()
                    # Animate through the real architectural phases
                    rendered_steps = []
                    for idx, step in enumerate(steps, start=1):
                        rendered_steps.append(f"**{step}**")
                        flow_box.markdown(
                            "<div class='flow-card'>" + "<br>".join(rendered_steps) + "</div>",
                            unsafe_allow_html=True
                        )
                        # Micro-pause so the human eye can observe the architectural progression
                        time.sleep(0.08)

            # Perform actual HTTP call
            try:
                start_time = time.time()
                response = send_support_question(user_question.strip())
                elapsed_ms = round((time.time() - start_time) * 1000, 2)

                if response.status_code == 201:
                    data = response.json()
                    st.success(f"**Support Response Received (HTTP 201 Created in {elapsed_ms}ms)**")

                    # Display Response in clean cards
                    col_user, col_assistant = st.columns(2)
                    with col_user:
                        st.info(f"**Customer Inquiry:**\n\n> {data.get('user_message')}")
                    with col_assistant:
                        st.success(f"**Bank Assistant Response:**\n\n{data.get('assistant_response')}")

                    # Display database persistence proof
                    st.markdown("#### Database Record Created")
                    col_id, col_time = st.columns(2)
                    col_id.metric(label="Database Assigned Record ID", value=f"#{data.get('id')}")
                    col_time.metric(label="Timestamp (UTC)", value=data.get('created_at', ''))

                elif response.status_code == 400:
                    detail = response.json().get("detail", "Invalid request")
                    st.error(f"API Bad Request (400): {detail}")
                elif response.status_code == 500:
                    detail = response.json().get("detail", "Internal server error")
                    st.error(f"API Server Error (500): {detail}")
                else:
                    st.error(f"Unexpected status ({response.status_code}): {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Connection Failed: Could not connect to FastAPI at http://127.0.0.1:8000.")
            except Exception as e:
                st.error(f"Unexpected Error: {str(e)}")


# ------------------------------------------------------------------------------
# TAB 2: Database Records (Accessed strictly through FastAPI)
# ------------------------------------------------------------------------------
with tab_history:
    st.markdown("### Stored Conversations in SQLite")
    st.write(
        "This table proves that conversations persist across requests in the SQLite database. "
        "**Notice:** The frontend fetched this data by calling `GET /api/conversations`. "
        "It did not open the SQLite `.db` file directly."
    )

    col_btn, col_info = st.columns([1, 4])
    refresh = col_btn.button("Refresh Records")

    if not api_healthy:
        st.warning("Start the FastAPI backend to retrieve database records.")
    else:
        try:
            res = fetch_recent_conversations(limit=25)
            if res.status_code == 200:
                records = res.json()
                if records:
                    st.write(f"Total retrieved: **{len(records)} conversations**")
                    # Format as clean table
                    table_data = []
                    for r in records:
                        table_data.append({
                            "Record ID": r.get("id"),
                            "User Inquiry": r.get("user_message"),
                            "Assistant Response": r.get("assistant_response"),
                            "Created At (UTC)": r.get("created_at")
                        })
                    st.dataframe(table_data, use_container_width=True)
                else:
                    st.info("No conversations in the database yet. Submit a question in Tab 1!")
            else:
                st.error(f"Failed to fetch records: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Error fetching history: {str(e)}")


# ------------------------------------------------------------------------------
# TAB 3: Architectural Concepts & Responsibilities
# ------------------------------------------------------------------------------
with tab_concepts:
    st.markdown("### Why Every Layer Exists")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown("""
        #### 1. Why doesn't Streamlit directly touch SQLite?
        - **Security:** In real systems, client apps run on user machines or mobile devices. If they connected directly to a database, you'd have to distribute database passwords to every user!
        - **Centralized Logic:** If you change a business rule (e.g. fee waiver criteria), you only update the service layer once.
        - **Concurrency & Scaling:** Direct database connections from frontends easily overwhelm database connection pools.

        #### 2. Why are API Schemas separate from Database Models?
        - **Database Models (`models.py`):** Define internal table storage (e.g., column types, foreign keys, sensitive hashes).
        - **API Schemas (`schemas/`):** Define the external network contract. They validate user inputs and control exactly what fields leave the server.
        """)

    with col_c2:
        st.markdown("""
        #### 3. Why does the Service Layer exist between Route & Database?
        - **Separation of Concerns:** Routes handle HTTP concerns (status codes, JSON parsing, URL routing).
        - **Reusability:** Business logic (support rules, AI reasoning, calculations) can be reused by APIs, background cron jobs, or CLI tools without duplicating SQL queries.

        #### 4. How does this map to Real Generative AI Systems?
        - In this project, `conversation_service.py` uses keyword rules.
        - In a production GenAI app, that exact function would call **Google Gemini**, **OpenAI**, or an **agent with RAG tools**.
        - The entire surrounding architecture (API, ORM, DB, Schemas) remains 100% identical!
        """)
