import os
from dotenv import load_dotenv

# Load environment variables from .env file

dotenv_path = '.env.local'

load_dotenv(dotenv_path=dotenv_path)

# Elasticsearch variables
ES_URL = os.environ.get("ES_URL")
ES_API_KEY = os.environ.get("ES_API_KEY")

# Vertex AI variables
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
TUNING_JOB_ID = os.environ.get("TUNING_JOB_ID")
KEY_PATH = os.environ.get("KEY_PATH")

#OpenAI variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_ID = os.environ.get("OPENAI_MODEL_ID")
HUMANLOOP_API_KEY = os.environ.get("HUMANLOOP_API_KEY")

