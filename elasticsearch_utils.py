from env import ES_URL, ES_API_KEY
from elasticsearch import Elasticsearch
import os
import json

ES_URL = os.environ.get("ES_URL")
ES_API_KEY = os.environ.get("ES_API_KEY")

es_client = Elasticsearch(ES_URL, api_key=ES_API_KEY)

def search_elasticsearch(user_input):
    """
    Search Elasticsearch using the text_expansion query with ELSER model.
    Parameters:
    user_input (str): The user's search query.

    Returns:
    None: Prints out the results or an error.
    """
    search_body = {
        "query": {
            "text_expansion": {
                "content_embedding": {
                    "model_id": ".elser_model_2_linux-x86_64",
                    "model_text": user_input
                }
            }
        },
        "size": 10
    }

    try:
        search_results = es_client.search(index="bayardcorpus", body=search_body)
        hits = search_results["hits"]["hits"]
        filtered_docs = []  # Create an empty list to store the filtered documents
        seen_titles = set()  # Create a set to keep track of seen titles
        print(f"Search query: {user_input}")
        print("Retrieved documents:")
        if not hits:
            print("No documents found.")
        for hit in hits:
            title = hit['_source'].get('title', 'No title provided')
            if title not in seen_titles:  # Check if the title has already been seen
                seen_titles.add(title)  # Add the title to the set of seen titles
                print(f"Score: {hit['_score']}")
                filtered_doc = {
                    'title': title,
                    'abstract': hit['_source'].get('abstract', 'No abstract available'),
                    'authors': hit['_source'].get('authors', 'No authors listed'),
                    'classification': hit['_source'].get('classification', 'No classification provided'),
                    'concepts': hit['_source'].get('concepts', 'No concepts listed'),
                    'yearPublished': hit['_source'].get('yearPublished', 'No year listed'),                    
                    'downloadUrl': hit['_source'].get('downloadUrl', 'No download URL provided'),
                    'emotion': hit['_source'].get('emotion', 'No emotion provided'),
                    'sentiment': hit['_source'].get('sentiment', 'No sentiment provided'),
                    'categories': hit['_source'].get('categories', 'No categories listed'),
                    '_id': hit['_source'].get('_id', 'No ID provided')
                }
                filtered_docs.append(filtered_doc)  # Append the filtered_doc dictionary to the list
                print(json.dumps(filtered_doc, indent=2))
        return filtered_docs  # Return the list of filtered documents
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an exception occurs
