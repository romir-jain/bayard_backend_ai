import os
import psycopg2
from typing import List, Dict

# Get the PostgreSQL connection URL from the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def log_conversation(input_text: str, model_output: str) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO conversations (input_text, model_output)
                VALUES (%s, %s)
            """, (input_text, model_output))
        conn.commit()

def get_conversation_history() -> List[Dict[str, str]]:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT input_text, model_output FROM conversations")
            rows = cur.fetchall()
            conversation_history = [
                {"input_text": row[0], "model_output": row[1]}
                for row in rows
            ]
    return conversation_history