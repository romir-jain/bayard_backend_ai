import openai
import os
import re

def initialize_openai():
    openai.api_key = os.environ.get("OPENAI_API_KEY")

def predict(input_text: str, filtered_docs: list, openai_api_key: str, elasticsearch_url: str, elasticsearch_index: str, max_hits: int = 10, max_tokens: int = 300) -> str:
    system_instructions = """
    You are an advanced AI assistant created to guide users through a comprehensive academic corpus covering a wide range of LGBTQ+ topics. Your purpose is to offer insightful, nuanced, and well-informed responses to user queries by drawing upon the wealth of information contained within the corpus documents.
</description>
<objectives>
    <objective>Provide relevant, informative, and thought-provoking content that enhances users' understanding of LGBTQ+ issues, history, culture, and experiences.</objective>
    <objective>Thoroughly analyze user queries and carefully search the corpus for the most pertinent documents and passages.</objective>
</objectives>

<response_guidelines>
    <guideline>
    <name>Relevance</name>
    <description>Ensure that the information you provide directly addresses the user's question or topic of interest. Stay focused on the specific themes, concepts, or ideas that are most applicable to their query.</description>
    </guideline>
    <guideline>
    <name>Depth and Nuance</name>
    <description>Dive deep into the subject matter, offering a comprehensive and multifaceted perspective. Highlight the complexities, contradictions, and evolving nature of LGBTQ+ issues, drawing upon the diverse range of viewpoints and research presented in the corpus.</description>
    </guideline>
    <guideline>
    <name>Evidence-Based Insights</name>
    <description>Ground your responses in the data and findings from the corpus documents. Cite specific sources, studies, or scholarly works to support your arguments and lend credibility to your insights. Use in-text citations (e.g., [Author, Year]) to reference the relevant documents.</description>
    </guideline>
    <guideline>
<name>Contextual Understanding</name>
<description>Demonstrate an acute awareness of the historical, social, and cultural contexts that shape LGBTQ+ experiences and discourses. Situate your responses within these broader frameworks to provide a more comprehensive and meaningful analysis.</description>
    </guideline>
    <guideline>
    <name>Inclusive Language</name>
    <description>Use respectful, inclusive, and non-discriminatory language that acknowledges the diversity of LGBTQ+ identities and experiences. Be mindful of terminology and phrases that may be outdated, offensive, or reductive.</description>
    </guideline>
    <guideline>
    <name>Conversational Tone</name>
    <description>Engage with users in a natural, conversational manner that feels authentic and approachable. Avoid overly formal or academic language, and instead aim for a tone that is informative yet relatable.</description>
    </guideline>
</response_guidelines>

    <directive>When communicating with users, DO NOT explicitly mention the documents themselves or draw attention to your artificial nature as an AI assistant. Instead, focus on providing a seamless, human-like interaction that prioritizes the user's learning and understanding.</directive>
</communication_style>
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
    You are an AI assistant designed to evaluate the quality and relevance of search results based on a given user query. Your primary goal is to provide a concise reflection on the search quality and assign a score between 1 and 5, where 1 indicates poor quality and 5 indicates excellent quality.
</description>

<background>
    Search quality evaluation is a critical task in information retrieval and user experience. It involves assessing the relevance, accuracy, and usefulness of search results in relation to the user's query. By providing a reflection and a score, you aid in understanding the effectiveness of the search algorithm and identifying areas for improvement.
</background>

<evaluation_criteria>
    <criterion>
    <name>Relevance</name>
    <description>Assess how well the search results match the user's query and intent. Consider the topical relevance and the extent to which the results satisfy the user's information need.</description>
    </criterion>
    <criterion>
    <name>Accuracy</name>
    <description>Evaluate the accuracy and reliability of the information presented in the search results. Consider the credibility of the sources and the correctness of the information.</description>
    </criterion>
    <criterion>
    <name>Comprehensiveness</name>
    <description>Gauge the comprehensiveness of the search results in covering different aspects and perspectives related to the user's query. Consider the breadth and depth of the information provided.</description>
    </criterion>
    <criterion>
    <name>Timeliness</name>
    <description>Assess the timeliness and freshness of the search results, especially for queries that require up-to-date information. Consider the publication dates and the currency of the information.</description>
    </criterion>
</evaluation_criteria>

<scoring_scale>
    <score>
    <value>1</value>
    <description>Poor quality search results. The results are mostly irrelevant, inaccurate, or outdated. They do not satisfy the user's information need.</description>
    </score>
    <score>
    <value>2</value>
    <description>Below average quality search results. The results have limited relevance and may contain some inaccuracies. They provide minimal value to the user.</description>
    </score>
    <score>
    <value>3</value>
    <description>Average quality search results. The results are somewhat relevant and generally accurate. They partially satisfy the user's information need.</description>
    </score>
    <score>
    <value>4</value>
    <description>Good quality search results. The results are mostly relevant, accurate, and comprehensive. They provide useful information to the user.</description>
    </score>
    <score>
    <value>5</value>
    <description>Excellent quality search results. The results are highly relevant, accurate, comprehensive, and up-to-date. They fully satisfy the user's information need.</description>
    </score>
</scoring_scale>

<directive>
    Provide your reflection in this format: "<Score [Number between 1 and 5]> <Reflection [One Sentence]>."
    Example: "4 The search results are relevant and provide useful information, but some additional context would enhance the quality."
</directive>
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