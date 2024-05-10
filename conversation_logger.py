import os
import psycopg2
from typing import List, Dict
import json

# Get the PostgreSQL connection URL from the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def log_conversation(input_text: str, model_output: str) -> None:
    input_text_json = json.dumps(input_text)
    model_output_json = json.dumps(model_output)
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO conversations (input_text, model_output)
                VALUES (%s, %s)
            """, (input_text_json, model_output_json))
        conn.commit()

def get_conversation_history() -> List[Dict[str, str]]:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT input_text, model_output FROM conversations")
            rows = cur.fetchall()
            conversation_history = [
                {
                    "input_text": json.loads(row[0]),
                    "model_output": json.loads(row[1])
                }
                for row in rows
            ]
    return conversation_history