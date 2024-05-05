import os
import logging
import uuid
import time
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from google.oauth2 import service_account
from elasticsearch_utils import search_elasticsearch
import json
import secrets
from supabase import create_client, Client
from openai_utils import initialize_openai, generate_model_output, generate_search_quality_reflection


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})

# Supabase PostgreSQL database connection
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are not set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_table_if_not_exists():
    runs_table = """
        CREATE TABLE IF NOT EXISTS runs (
            run_id VARCHAR(255) PRIMARY KEY,
            timestamp BIGINT,
            input_text TEXT,
            model_output TEXT
        );
    """
    supabase.postgrest.rpc("create_table", {
        "name": "runs",
        "columns": [
            {"name": "run_id", "type": "VARCHAR(255)"},
            {"name": "timestamp", "type": "BIGINT"},
            {"name": "input_text", "type": "TEXT"},
            {"name": "model_output", "type": "TEXT"}
        ],
        "primary_key": ["run_id"]
    })

    api_keys_table = """
        CREATE TABLE IF NOT EXISTS api.keys (
            api_key VARCHAR(255) PRIMARY KEY
        );
    """
    supabase.postgrest.rpc("create_table", {
        "name": "keys",
        "columns": [
            {"name": "api_key", "type": "VARCHAR(255)"}
        ],
        "primary_key": ["api_key"]
    })

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
    try:
        # Generate a new API key
        new_api_key = secrets.token_urlsafe(32)
        # Store the new API key in the database
        data = supabase.table("keys").insert({"api_key": new_api_key}).execute()

        # Check if the insertion was successful
        if data:
            return jsonify({"api_key": new_api_key}), 200
        else:
            raise Exception("Failed to store API key in the database")
    except Exception as e:
        logging.error(f"Failed to generate API key: {str(e)}")
        return jsonify({"error": "Failed to generate API key"}), 500

@app.before_request
def authenticate_request():
    # Check if the request is for the health check or API key generation endpoint
    if request.path == '/health-check' or request.path == '/api/generate-key':
        return

    # Try to get the API key from the environment variable
    bayard_api_key = os.environ.get('BAYARD_API_KEY')
    logging.info(f"Retrieved API key from environment variable: {bayard_api_key}")

    # If the environment variable is not set, try to get the API key from the X-API-Key header
    if not bayard_api_key:
        bayard_api_key = request.headers.get('X-API-Key')
        logging.info(f"Retrieved API key from X-API-Key header: {bayard_api_key}")

    # If neither the environment variable nor the X-API-Key header is present, try to get the API key from the Authorization header
    if not bayard_api_key:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer'):
            bayard_api_key = auth_header.split(' ')[1]
            logging.info(f"Retrieved API key from Authorization header: {bayard_api_key}")

    if not bayard_api_key:
        logging.error("API key not found in request headers or environment variable")
        return jsonify({'error': 'API key not configured'}), 500

    # Check if the API key exists in the database
    api_key_exists = supabase.table("keys").select("api_key").ilike("api_key", bayard_api_key).execute()    
    logging.info(f"API key exists in database: {api_key_exists.data}")
    if not api_key_exists.data:
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

    # Generate search quality reflection and score
    search_quality = generate_search_quality_reflection(search_results, input_text)

    # Generate model output
    model_output = generate_model_output(input_text, search_results)

    # Store the run in the database
    supabase.table("runs").insert({
        "run_id": run_id,
        "timestamp": timestamp,
        "input_text": input_text,
        "model_output": model_output
    }).execute()

    response_data = {
        "run_id": run_id,
        "timestamp": timestamp,
        "input_text": input_text,
        "model_output": model_output,
        "search_quality_reflection": search_quality["search_quality_reflection"],
        "search_quality_score": search_quality["search_quality_score"],
        "documents": [{
                "abstract": doc.get("abstract", "No abstract provided"),
                "authors": doc.get("authors", ["No authors provided"]),
                "categories": doc.get("categories", ["No categories provided"]),
                "classification": doc.get("classification", "No classification provided"),
                "concepts": doc.get("concepts", ["No concepts provided"]),
                "downloadUrl": doc.get("downloadUrl", "No download URL provided"),
                "emotion": doc.get("emotion", "No emotion provided"),
                "id": doc.get("_id", "No ID provided"),
                "sentiment": doc.get("sentiment", "No sentiment provided"),
                "title": doc.get("title", "No title provided"),
                "yearPublished": doc.get("yearPublished", "No year published provided")
                } for doc in (search_results or [])
    ]}

    return jsonify(response_data)                    
                    
                    
if __name__ == "__main__":
    create_table_if_not_exists()
    app.run(host="0.0.0.0", port=10000, debug=True)