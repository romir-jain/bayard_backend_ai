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

@app.route("/api/bayard", methods=["POST"])
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
    app.run(host="0.0.0.0", port=5555, debug=True)