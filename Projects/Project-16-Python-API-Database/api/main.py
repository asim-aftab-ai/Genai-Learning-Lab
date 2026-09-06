"""
================================================================================
THIS FILE'S JOB IS TO SERVE AS THE FASTAPI APPLICATION ENTRY POINT
================================================================================

1. Why this file exists:
   Every backend server needs an entry point—the central conductor that initializes
   the web framework, attaches configuration, starts up services (like the database),
   and mounts the API route handlers.

2. What it does:
   - Instantiates the `FastAPI` application instance.
   - Configures application metadata (title, description, version).
   - Initializes database tables on startup via `init_db()`.
   - Registers the endpoint router from `api/routes.py`.
   - Optionally allows direct execution using `python -m api.main`.

3. Who communicates with it:
   - Uvicorn (ASGI web server) starts and runs this `app`.
   - Frontend clients (Streamlit) send HTTP traffic directed at this application.

4. What it sends to the next layer:
   - Routes incoming HTTP requests to `api/routes.py`.

5. What it receives back:
   - Receives serialized HTTP responses from routes to send over the network.
================================================================================
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Ensure the Project-16 root is on sys.path so modules can import seamlessly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from database.connection import init_db
from api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan Context Manager.
    - Code before `yield` runs on server startup:
      We initialize our SQLite tables here.
    - Code after `yield` runs on server shutdown:
      Cleanup tasks would go here.
    """
    print(">> [Startup] Initializing SQLite database tables...")
    init_db()
    print(">> [Startup] Database ready. Bank Support API listening.")
    yield
    print(">> [Shutdown] Bank Support API stopping.")


# Create FastAPI application instance
app = FastAPI(
    title="Bank Customer Support API",
    description=(
        "Educational FastAPI backend demonstrating clean multi-layer architecture: "
        "Streamlit -> FastAPI -> Service -> SQLAlchemy -> SQLite."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Register API routes defined in api/routes.py
app.include_router(router)


@app.get("/", summary="Root Documentation Link")
def root():
    """
    Convenient landing endpoint directing developers to interactive Swagger API docs.
    """
    return {
        "message": "Welcome to the Bank Customer Support API",
        "docs_url": "/docs",
        "health_check": "/api/health",
        "conversations": "/api/conversations"
    }


if __name__ == "__main__":
    import uvicorn
    # Allows starting the server directly: python -m api.main
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
