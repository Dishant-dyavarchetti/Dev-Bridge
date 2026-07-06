import os
import logging
import psycopg

logger = logging.getLogger("devbridge." + __name__)

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return None
    try:
        conn = psycopg.connect(db_url)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Neon database: {e}")
        return None

def init_db():
    """Initializes the database and creates necessary tables if they do not exist."""
    conn = get_db_connection()
    if not conn:
        logger.info("No active database connection found. Database caching disabled.")
        return
        
    try:
        with conn.cursor() as cur:
            # Create repository metadata cache table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS repository_cache (
                    repo_name VARCHAR(255) PRIMARY KEY,
                    language VARCHAR(100),
                    structure TEXT,
                    frameworks TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Create session history table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS session_history (
                    session_id VARCHAR(255) PRIMARY KEY,
                    user_request TEXT,
                    workflow_state TEXT,
                    outputs TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            logger.info("Neon database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error during database table initialization: {e}")
    finally:
        conn.close()

def save_repository_to_cache(repo_name: str, language: str, structure: str, frameworks: str):
    """Saves codebase analysis metadata to Neon database."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO repository_cache (repo_name, language, structure, frameworks, updated_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (repo_name) DO UPDATE 
                SET language = EXCLUDED.language,
                    structure = EXCLUDED.structure,
                    frameworks = EXCLUDED.frameworks,
                    updated_at = CURRENT_TIMESTAMP;
            """, (repo_name, language, structure, frameworks))
            conn.commit()
            logger.info(f"Repository '{repo_name}' saved to Neon cache.")
    except Exception as e:
        logger.error(f"Error saving repository '{repo_name}' to Neon cache: {e}")
    finally:
        conn.close()

def get_repository_from_cache(repo_name: str) -> dict | None:
    """Fetches codebase analysis metadata from Neon database cache."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT language, structure, frameworks FROM repository_cache WHERE repo_name = %s", (repo_name,))
            row = cur.fetchone()
            if row:
                return {
                    "language": row[0],
                    "structure": row[1],
                    "frameworks": row[2]
                }
            return None
    except Exception as e:
        logger.error(f"Error fetching repository '{repo_name}' from Neon cache: {e}")
        return None
    finally:
        conn.close()

def save_session_history(session_id: str, user_request: str, workflow_state: str, outputs: str):
    """Persists current session state to Neon database."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO session_history (session_id, user_request, workflow_state, outputs, updated_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (session_id) DO UPDATE 
                SET user_request = EXCLUDED.user_request,
                    workflow_state = EXCLUDED.workflow_state,
                    outputs = EXCLUDED.outputs,
                    updated_at = CURRENT_TIMESTAMP;
            """, (session_id, user_request, workflow_state, outputs))
            conn.commit()
            logger.info(f"Session '{session_id}' state saved to Neon.")
    except Exception as e:
        logger.error(f"Error saving session '{session_id}' state: {e}")
    finally:
        conn.close()
