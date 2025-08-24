## Project Structure

The project consists of the following main files:

- `app.py`: The main Flask application file that handles the API endpoints and integrates with Vertex AI and Elasticsearch.
- `vertex_ai_utils.py`: Utility functions for initializing Vertex AI and generating model output.
- `elasticsearch_utils.py`: Utility functions for searching Elasticsearch.
- `requirements.txt`: The list of Python dependencies required for the project.

## Installation

Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

The project requires the following environment variables to be set:

- `PROJECT_ID`: The ID of your Google Cloud project.
- `SECRET_URI`: The URI of the Google Secret Manager secret containing the service account key.

Make sure to set these environment variables before running the application.

## Usage

To start the Flask application, run the following command:
```
python app.py
```

The application will be accessible at `http://localhost:8080`.

### API Endpoint

- `/api/bayard` (POST):
  - Description: Processes the user input, searches Elasticsearch for relevant documents, and generates model output using Vertex AI.
  - Request Body:
    ```json
    {
      "input_text": "Your question here"
    }
    ```
  - Response:
    ```json
    {
      "modelOutput": "Generated model output"
    }
    ```

