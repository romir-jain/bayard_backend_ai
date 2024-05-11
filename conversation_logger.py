import os
import psycopg2
from typing import List, Dict
import json

# Get the PostgreSQL connection URL from the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def log_conversation(input_text: str, model_output: str, response_quality_scores: Dict[str, int]) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO conversations (
                    input_text,
                    model_output,
                    relevance_score,
                    coherence_score,
                    informativeness_score,
                    engagement_score,
                    overall_score
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (input_text,
                    model_output,
                    response_quality_scores.get('Relevance') if response_quality_scores else None,
                    response_quality_scores.get('Coherence') if response_quality_scores else None,
                    response_quality_scores.get('Informativeness') if response_quality_scores else None,
                    response_quality_scores.get('Engagement') if response_quality_scores else None,
                    response_quality_scores.get('Overall Score') if response_quality_scores else None
                    ))
        conn.commit()