import openai
import os
import re

def initialize_openai():
    openai.api_key = os.environ.get("OPENAI_API_KEY")

def predict(input_text: str, filtered_docs: list, openai_api_key: str, elasticsearch_url: str, elasticsearch_index: str, max_hits: int = 10, max_tokens: int = 300) -> str:
    system_instructions = """
    You are an AI assistant designed to help users explore and understand an extensive academic corpus on LGBTQ+ topics.
    Your primary objective is to provide relevant information, insights, and perspectives from the documents in the corpus,
    while maintaining a natural, conversational tone that avoids explicitly referring to the documents themselves or your artificial nature.
    """

    model_input = f"User Query: {input_text}\n\n"
    model_input += "Retrieved Documents:\n"
    total_tokens = len(input_text.split())

    if not filtered_docs:
        model_input += "No relevant documents found.\n"
    else:
        for i, doc in enumerate(filtered_docs[:max_hits]):
            model_input += f"Document {i+1}:\n"
            model_input += f"Title: {doc['title']}\n"
            model_input += f"Authors: {', '.join(map(str, doc['authors']))}\n"
            model_input += f"Content: {doc['abstract']}\n"
            model_input += f"Classification: {doc['classification']}\n"
            model_input += f"Concepts: {', '.join(map(str, doc['concepts']))}\n"
            model_input += f"Emotion: {doc['emotion']}\n"
            model_input += f"Year Published: {doc['yearPublished']}\n"
            model_input += f"Download URL: {doc['downloadUrl']}\n"
            model_input += f"Sentiment: {doc['sentiment']}\n"
            model_input += f"Categories: {', '.join(map(str, doc['categories']))}\n"
            model_input += f"ID: {doc['_id']}\n\n"

    model_input += "Based on the user's query and the retrieved documents, provide a helpful response.\n\nResponse:"

    # Use OpenAI's GPT-4 model to generate a response
    response = openai.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL_ID"),
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": model_input}
        ],
        max_tokens=max_tokens
    )

    model_output = response.choices[0].message.content

    return model_output

# Generate model output
def generate_model_output(input_text: str, filtered_docs: list, max_hits: int = 10, max_tokens: int = 300) -> str:
    return predict(
        input_text,
        filtered_docs,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        elasticsearch_url=os.environ.get("ES_URL"),
        elasticsearch_index="bayardcorpus",
        max_hits=max_hits,
        max_tokens=max_tokens
    )

def generate_search_quality_reflection(search_results: list, input_text: str) -> dict:
    system_instructions = """
    You are an AI assistant designed to evaluate the quality and relevance of search results based on a given user query.
    Your task is to provide a reflection on the search quality and assign a score between 1 and 5, where 1 indicates poor quality and 5 indicates excellent quality.
    
    <Directive>Provide your reflection in this format: "<Score [Number between 1 and 5]> <Reflection [One Sentence]>."</Directive>
    
    """

    search_quality_prompt = f"User Query: {input_text}\n\n"
    search_quality_prompt += "Search Results:\n"

    for i, doc in enumerate(search_results):
        search_quality_prompt += f"Document {i+1}:\n"
        search_quality_prompt += f"Title: {doc.get('title', 'No title provided')}\n"
        search_quality_prompt += f"Abstract: {doc.get('abstract', 'No abstract provided')}\n\n"

    search_quality_prompt += "Based on the user query and the provided search results, please provide a reflection on the quality and relevance of the search results. Also, assign a search quality score between 1 and 5, where 1 indicates poor quality and 5 indicates excellent quality.\n\nReflection:"

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=system_instructions + "\n\n" + search_quality_prompt,
        max_tokens=150
    )

    reflection_output = response.choices[0].text.strip()
    score_match = re.search(r'(\d+)', reflection_output)
    score = int(score_match.group(1)) if score_match else None

    return {
        "search_quality_reflection": reflection_output,
        "search_quality_score": score
    }