"""
================================================================================
THIS FILE'S JOB IS TO MANAGE DATABASE CONNECTION AND SESSIONS
================================================================================

1. Why this file exists:
   Every application needs a single, centralized place to configure how it connects
   to its persistent data store. Putting database connection details in routes or
   services causes duplicate code and makes changing databases difficult.

2. What it does:
   - Sets up the SQLite database file path.
   - Creates the SQLAlchemy Engine (the low-level connection pool).
   - Creates the SessionLocal factory (used to produce database sessions).
   - Provides `init_db()` to automatically create database tables on startup.
   - Provides `get_db()` as a dependency generator for FastAPI endpoints.

3. Who communicates with it:
   - `api/main.py` calls `init_db()` when the backend starts up.
   - `api/routes.py` calls `get_db()` via FastAPI's `Depends` to obtain a DB session.
   - `database/models.py` uses the shared `Base` declarative class.

4. What it sends to the next layer:
   - Provides an active SQLAlchemy `Session` object to the API route and service layer.

5. What it receives back:
   - When the session finishes its work, this file closes the session cleanly.
================================================================================
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ------------------------------------------------------------------------------
# 1. Database Location & URL Configuration
# ------------------------------------------------------------------------------
# We store the SQLite database file directly in the Project-16 directory
# using an absolute path relative to this file. This prevents issues where
# starting the app from different working directories creates misplaced DB files.
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "bank_support.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# ------------------------------------------------------------------------------
# 2. SQLAlchemy Engine & Session Configuration
# ------------------------------------------------------------------------------
# The 'engine' is the core interface to the database.
# 'check_same_thread=False' is needed only for SQLite because FastAPI handles
# requests across multiple threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is our session factory. Each API request gets its own separate session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models (tables) to inherit from.
Base = declarative_base()


# ------------------------------------------------------------------------------
# 3. Table Initialization Helper
# ------------------------------------------------------------------------------
def init_db():
    """
    Creates all database tables defined in database/models.py if they do not already exist.
    Called once when the FastAPI server boots up.
    """
    # Import models here so Base knows about all registered tables before creating them
    import database.models  # noqa: F401
    Base.metadata.create_all(bind=engine)


# ------------------------------------------------------------------------------
# 4. FastAPI Dependency Generator for Database Sessions
# ------------------------------------------------------------------------------
def get_db():
    """
    Dependency function for FastAPI.
    Yields an independent database session for a single request,
    and guarantees the session is closed when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
