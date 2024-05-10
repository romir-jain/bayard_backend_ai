import openai

def classify_query(query):
    prompt = f"""
    Classify the following user query as either 'search' or 'conversation' based on the provided examples and guidelines:

    Guidelines:
    - If the user's query is a request for information, documents, or resources related to LGBTQIA+ topics, classify it as 'search'.
    - If the user's query is completely unrelated to LGBTQIA+ topics or is a follow-up question on previously discussed documents, classify it as 'conversation'.
    - In all other cases, classify the query as 'search' to prioritize providing relevant information from the corpus.

    Examples:
    - Query: "What are some important LGBTQIA+ historical events?"
      Classification: search
    - Query: "Are there any research papers on the experiences of transgender individuals in the workplace?"
      Classification: search
    - Query: "Can you recommend some LGBTQIA+ inclusive children's books?"
      Classification: search
    - Query: "What are the key provisions of the Equality Act?"
      Classification: search
    - Query: "How has the media representation of LGBTQIA+ characters evolved over time?"
      Classification: search
    - Query: "What are some notable LGBTQIA+ organizations and their missions?"
      Classification: search
    - Query: "Can you provide statistics on LGBTQIA+ mental health disparities?"
      Classification: search
    - Query: "What are the legal rights and protections for LGBTQIA+ individuals in the workplace?"
      Classification: search
    - Query: "Can you explain the difference between sexual orientation and gender identity?"
      Classification: search
    - Query: "What's the weather like today?"
      Classification: conversation
    - Query: "I'm looking for a good Italian restaurant nearby. Any suggestions?"
      Classification: conversation
    - Query: "In the research paper you mentioned earlier about transgender experiences, what were the key findings?"
      Classification: conversation
    - Query: "Can you tell me more about the LGBTQIA+ inclusive children's book you recommended in our previous discussion?"
      Classification: conversation

    Query: {query}
    Classification:
    """
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )
    classification = response.choices[0].text.strip().lower()
    return classification