import openai
import os

def evaluate_response_quality(input_text: str, model_output: str) -> dict:
    system_message = f"""
    You are an AI assistant named ResponseQualityEvaluator. Your task is to evaluate the quality of the model's response based on the given input text and the model's generated output.

    Evaluate the response quality based on the following criteria:
    1. Relevance: How relevant is the model's response to the input text?
    2. Coherence: Is the model's response coherent and well-structured?
    3. Informativeness: Does the model's response provide informative and useful information?
    4. Engagement: Is the model's response engaging and encourages further interaction?

    For each criterion, provide a score between 1 and 5, where:
    - 1 indicates poor quality
    - 3 indicates average quality
    - 5 indicates excellent quality

    Additionally, provide an overall score between 1 and 5 for the model's response quality.

    Please format your evaluation as follows:
    Relevance: <score[integer]>
    Coherence: <score[integer]>
    Informativeness: <score[integer]>
    Engagement: <score[integer]>
    Overall Score: <score[integer]>

    Input Text: {input_text}
    Model Output: {model_output}
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Input Text: {input_text}\nModel Output: {model_output}"}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    evaluation_text = response.choices[0].message.content.strip()

    evaluation_scores = {}
    for line in evaluation_text.split("\n"):
        if ":" in line:
            criterion, score = line.split(":")
            evaluation_scores[criterion.strip()] = int(score.strip())

    return evaluation_scores