# Bayard: Open-Source LGBTQIA+ AI Research Assistant

Bayard is an open-source AI assistant that retrieves, analyzes, and contextualizes LGBTQIA+ research from the Bayard Corpus, a collection of open-source LGBTQIA+-focused materials. The goal of this project is to make LGBTQIA+ research more accessible, contextualize findings, and make it easier to uncover insights.

## Project Structure

The project consists of the following main files:

- `app.py`: The main Flask application file that handles the API endpoints and integrates with Vertex AI and Elasticsearch.
- `vertex_ai_utils.py`: Utility functions for initializing Vertex AI and generating model output.
- `elasticsearch_utils.py`: Utility functions for searching Elasticsearch.
- `requirements.txt`: The list of Python dependencies required for the project.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jweaver9/bayard.git
   ```

2. Install the required dependencies:
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

## Accessing the API

You can access the Bayard API via a POST request to the following URL:
```
https://bayardapp.onrender.com/api/bayard
```

To make a request, send a POST request to the above URL with the following JSON payload:
```json
{
  "input_text": "Your question here"
}
```

Replace `"Your question here"` with the actual question or input text you want to process.

The API will respond with a JSON object containing the generated model output:
```json
{
  "modelOutput": "Generated model output"
}
```

## Dependencies

Bayard relies on several dependencies to function properly. These dependencies are listed in the `requirements.txt` file, which includes the necessary Python packages and their versions. Some of the key dependencies are:

- `flask`: A lightweight web framework used to build the API endpoints and handle HTTP requests.
- `flask_cors`: A Flask extension that handles Cross-Origin Resource Sharing (CORS) to allow requests from different domains.
- `google-auth` and `google-oauth2`: Libraries for authentication and authorization with Google Cloud services.
- `google-cloud-aiplatform`: The Google Cloud Vertex AI library for generating model outputs.
- `google-cloud-storage`: A library for interacting with Google Cloud Storage to access the corpus data.
- `elasticsearch`: A library for interacting with Elasticsearch to search and retrieve relevant documents from the corpus.

To install the dependencies, run the following command:
```
pip install -r requirements.txt
```

Make sure you have Python installed on your system before running the above command.

## Accessing the Bayard Corpus

The Bayard Corpus, which is a collection of open-source LGBTQIA+-focused materials, can be accessed via the MongoDB Data API endpoint. The corpus data is stored in a MongoDB database and can be retrieved using HTTP requests to the following URL:
```
https://us-east-2.aws.data.mongodb-api.com/app/data-milzl/endpoint/data/v1
```

To access the corpus data, follow these steps:

1. Set the appropriate HTTP method (GET, POST, PUT, DELETE) based on the desired operation.

2. Include the necessary request headers:
   - `Content-Type: application/json`: Specifies the content type of the request payload as JSON.
   - `api-key: <your-api-key>`: Replaces `<your-api-key>` with your actual MongoDB Data API key for authentication.

3. Construct the request payload in JSON format, providing the required data for the specific operation.

4. Send the HTTP request to the API endpoint using a tool like cURL, Postman, or a programming language of your choice.

Here's an example of making a GET request to retrieve documents from the Bayard Corpus using cURL:

```bash
curl -X GET \
  'https://us-east-2.aws.data.mongodb-api.com/app/data-milzl/endpoint/data/v1' \
  -H 'Content-Type: application/json' \
  -H 'api-key: <your-api-key>' \
  -d '{
    "collection": "corpus",
    "filter": {
      "category": "research"
    },
    "limit": 10
  }'
```

Make sure to replace `<your-api-key>` with your actual MongoDB Data API key.

In the above example, we are retrieving documents from the `corpus` collection where the `category` field is set to `"research"`. The `limit` parameter specifies the maximum number of documents to return.

The API will process the request and respond with the matching documents from the corpus in JSON format:

```json
{
  "documents": [
    {
      "_id": "<document-id>",
      "title": "Document Title",
      "content": "Document content goes here...",
      "category": "research"
    },
    ...
  ]
}
```

Note: Ensure that you keep your API key secure and do not share it publicly. It is recommended to use environment variables or secure configuration files to store your API key.

For more detailed information on using the MongoDB Data API and constructing requests, refer to the MongoDB Data API documentation: [https://www.mongodb.com/docs/atlas/api/data-api/](https://www.mongodb.com/docs/atlas/api/data-api/)

## Contributing

Contributions to Bayard are welcome! If you're interested in collaborating or have suggestions for improvements, please reach out or submit a pull request.

We are actively seeking collaborators to help refine the AI, improve its usability, and ensure it's unbiased and inclusive. If you're a researcher, ethnographer, or web developer (especially with TypeScript experience), we'd love to hear from you.

## Future Enhancements

- Conduct a more robust analysis to test the diversity of the materials in the Bayard Corpus.
- Continuously evaluate and report on Bayard's biases to maintain transparency and accountability.
- Develop a user-friendly web interface for Bayard.

## License

This project is licensed under the [MIT License](LICENSE).
