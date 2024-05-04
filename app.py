import os
import uuid
import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from google.auth import credentials
from google.oauth2 import service_account
from openai_utils import initialize_openai, generate_model_output
from elasticsearch_utils import search_elasticsearch
import json
import psycopg2
import time
import secrets


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "headers": ["Content-Type", "Authorization"]}})

# Render PostgreSQL database connection
db_connection = psycopg2.connect(
    host="dpg-col8gja1hbls73b5gl50-a.oregon-postgres.render.com",
    port="5432",
    database="bayard",
    user="bayard_user",
    password=os.environ.get("DB_PASSWORD")
)

def create_table_if_not_exists():
    with db_connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_runs (
                run_id VARCHAR(255) PRIMARY KEY,
                timestamp BIGINT,
                input_text TEXT,
                model_output TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                api_key VARCHAR(255) PRIMARY KEY
            );
        """)
    db_connection.commit()

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

key_path = "key.json"

# Load the credentials from the key.json file
try:
    with open(key_path, "r") as f:
        key_data = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(key_data)
except FileNotFoundError:
    print(f"Key file {key_path} not found. Please provide a valid key file.")
    exit(1)

initialize_openai()

@app.route("/health-check", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/api/bayard", methods=["OPTIONS"])
def handle_preflight_request():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response

@app.route("/api/generate-key", methods=["GET"])
def generate_api_key():
    # Generate a new API key
    new_api_key = secrets.token_urlsafe(32)
    # Store the new API key in the database
    with db_connection.cursor() as cursor:
        cursor.execute("INSERT INTO api_keys (api_key) VALUES (%s)", (new_api_key,))
    db_connection.commit()

    return jsonify({"api_key": new_api_key})

@app.before_request
def authenticate_request():
    # Check if the request is for the health check or API key generation endpoint
    if request.path == '/health-check' or request.path == '/api/generate-key':
        return

    # Try to get the API key from the environment variable
    bayard_api_key = os.environ.get('BAYARD_API_KEY')

    # If the environment variable is not set, try to get the API key from the X-API-Key header
    if not bayard_api_key:
        bayard_api_key = request.headers.get('X-API-Key')

    # If neither the environment variable nor the X-API-Key header is present, try to get the API key from the Authorization header
    if not bayard_api_key:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            bayard_api_key = auth_header.split(' ')[1]

    if not bayard_api_key:
        return jsonify({'error': 'API key not configured'}), 500

    # Check if the API key exists in the database
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM api_keys WHERE api_key = %s", (bayard_api_key,))
        if not cursor.fetchone():
            return jsonify({'error': 'Invalid API key'}), 401

    # Check if the rate limit has been exceeded
    if not rate_limit(bayard_api_key):
        return jsonify({'error': 'Rate limit exceeded'}), 429

# Dictionary to store API key usage
api_key_usage = {}

# Rate limiting configuration
RATE_LIMIT_QUERIES = 500
RATE_LIMIT_PERIOD = 3600  # 1 hour in seconds

def rate_limit(api_key):
    current_time = datetime.datetime.now()
    usage_history = api_key_usage.get(api_key, [])

    # Remove expired entries from the usage history
    usage_history = [entry for entry in usage_history if (current_time - entry).total_seconds() < RATE_LIMIT_PERIOD]
    api_key_usage[api_key] = usage_history

    # Check if the rate limit has been exceeded
    if len(usage_history) >= RATE_LIMIT_QUERIES:
        return False

    # Add the current request to the usage history
    usage_history.append(current_time)
    api_key_usage[api_key] = usage_history

    return True

@app.route("/api/bayard", methods=["POST"])
def bayard_api():
    input_text = request.json.get("input_text")
    if not input_text:
        return jsonify({"error": "Input text is required"}), 400

    run_id = str(uuid.uuid4())
    timestamp = int(time.time())

    # Search Elasticsearch for relevant documents
    search_results = search_elasticsearch(input_text)

    # Generate model output using OpenAI
    model_output = generate_model_output(input_text, search_results or [])

    # Store the run in the database
    with db_connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO model_runs (run_id, timestamp, input_text, model_output) VALUES (%s, %s, %s, %s)",
            (run_id, timestamp, input_text, model_output),
        )
    db_connection.commit()

    # Prepare the response in the desired format
    response_data = {
        "modelOutput": model_output,
        "relevantDocuments": [
            {
                "_id": doc.get("_id", "No ID provided"),
                "abstract": doc.get("abstract", "No abstract provided"),
                "authors": doc.get("authors", ["No authors listed"]),
                "categories": doc.get("categories", "No categories listed"),
                "classification": doc.get("classification", "No classification provided"),
                "concepts": doc.get("concepts", "No concepts listed"),
                "downloadUrl": doc.get("downloadUrl", "No download URL provided"),
                "emotion": doc.get("emotion", "No emotion provided"),
                "sentiment": doc.get("sentiment", "No sentiment provided"),
                "title": doc.get("title", "No title provided"),
                "yearPublished": doc.get("yearPublished", "No year published provided")
            } for doc in (search_results or [])
        ],
        "runId": run_id,
        "timestamp": timestamp
    }

    return jsonify(response_data)

if __name__ == "__main__":
    create_table_if_not_exists()
    app.run(host="0.0.0.0", port=8080, debug=True)