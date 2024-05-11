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
    list: A list of filtered documents as dictionaries, or None if an exception occurs.
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
        filtered_docs = []
        seen_titles = set()

        for hit in hits:
            title = hit['_source'].get('title', 'No title provided')
            if title not in seen_titles:
                seen_titles.add(title)
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
                    '_id': hit['_source'].get('_id', 'No ID provided'),
                    '_score': hit['_score']
                }
                filtered_docs.append(filtered_doc)

        return filtered_docs

    except Exception as e:
        print(f"An error occurred: {e}")
        return None