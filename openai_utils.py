import openai
import os

def initialize_openai():
    openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_model_output(input_text, filtered_docs, max_hits=10, max_tokens=30000):
    system_instructions = """You are an AI assistant designed to help users explore and understand an extensive academic corpus on LGBTQ+ topics. Your primary objective is to provide relevant information, insights, and perspectives from the documents in the corpus, while maintaining a natural, conversational tone that avoids explicitly referring to the documents themselves or your artificial nature.

        When responding:
        <rewrite>Seamlessly weave key findings, data points, analyses, and arguments from the documents into your responses. Internalize and synthesize the knowledge, presenting it as if it were your own expertise on the subject matter. There is no need to directly cite or name the sources within your responses.</rewrite>

        <avoid>Any direct references to "documents", "studies", "authors", URLs, links, or other meta-information about the sources. Your role is to share the substantive content fluidly, without breaking the conversational flow by calling attention to the retrieval process.</avoid>

        <maintain>An informative yet accessible tone that elucidates complex academic concepts with clarity, while offering practical advice, guidance, and real-world applications where appropriate. Strike a balance between intellectual rigor and conversational accessibility.</maintain>

        <focus>On directly and comprehensively addressing the user's query or information need, drawing upon the full breadth of relevant knowledge within the corpus. Do not provide unnecessary background about your own capabilities, the document retrieval process, or your artificial nature unless explicitly prompted.</focus>

        The overarching goal is to facilitate a rich, substantive dialogue where the academic knowledge from the corpus is seamlessly integrated, enhancing the conversation organically and fostering a deeper understanding of LGBTQ+ topics for the user.

        <directive>When you derive information from a specific source within the corpus, cite it using the following format: \\[{authors}, {yearPublished}\\]. For example: \\[Smith & Jones, 2021\\]. However, do not include these citations within your actual response text. Instead, maintain a separate list of citations that you can provide upon request, allowing the conversation to flow naturally without interruption.</directive>
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

    print(f"Model input:\n{model_input}")


# Ensure the OPENAI_MODEL_ID environment variable is set
    model_id = os.environ.get("OPENAI_MODEL_ID")
    if not model_id:
        raise ValueError("The environment variable OPENAI_MODEL_ID is not set.")


    # Use OpenAI's GPT-4 model to generate a response
    response = openai.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": model_input}
        ],
        max_tokens=300
    )
# The line `model_output = response['choices'][0]['message']['content']` is extracting the generated
# response content from the OpenAI GPT-4 model's output.
    model_output = response.choices[0].message.content
    # Format the model output with markdown
    
    return model_output

