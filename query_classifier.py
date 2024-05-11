import os
import cohere
from cohere import ClassifyExample

# Initialize Cohere client
co = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

def classify_query(query):
    # Define examples for classification
    examples = [
        ClassifyExample(text="What are some important LGBTQIA+ historical events?", label="search"),
        ClassifyExample(text="Are there any research papers on the experiences of transgender individuals in the workplace?", label="search"),
        ClassifyExample(text="Can you recommend some LGBTQIA+ inclusive children's books?", label="search"),
        ClassifyExample(text="What are the key provisions of the Equality Act?", label="search"),
        ClassifyExample(text="How has the media representation of LGBTQIA+ characters evolved over time?", label="search"),
        ClassifyExample(text="What are some notable LGBTQIA+ organizations and their missions?", label="search"),
        ClassifyExample(text="Can you provide statistics on LGBTQIA+ mental health disparities?", label="search"),
        ClassifyExample(text="What are the legal rights and protections for LGBTQIA+ individuals in the workplace?", label="search"),
        ClassifyExample(text="Can you explain the difference between sexual orientation and gender identity?", label="search"),
        ClassifyExample(text="Tell me more about the impact of LGBTQIA+ advocacy on recent legislation.", label="search"),
        ClassifyExample(text="Discuss the role of LGBTQIA+ activists in the civil rights movement.", label="search"),
        ClassifyExample(text="Can you list some influential LGBTQIA+ figures in technology?", label="search"),
        ClassifyExample(text="What advancements have been made in LGBTQIA+ rights over the last decade?", label="search"),
        ClassifyExample(text="Explain the significance of Pride Month and its global impact.", label="search"),
        ClassifyExample(text="What are the challenges faced by LGBTQIA+ youth in educational institutions?", label="search"),
        ClassifyExample(text="How do different cultures view and treat LGBTQIA+ individuals?", label="search"),
        ClassifyExample(text="Can you detail the evolution of LGBTQIA+ representation in media?", label="search"),
        ClassifyExample(text="What are the current debates surrounding transgender athletes in sports?", label="search"),
        ClassifyExample(text="Describe the influence of LGBTQIA+ communities on popular culture.", label="search"),
        ClassifyExample(text="What are the psychological effects of discrimination on LGBTQIA+ individuals?", label="search"),
        ClassifyExample(text="How do LGBTQIA+ rights vary by country?", label="search"),
        ClassifyExample(text="What support systems are available for LGBTQIA+ people facing homelessness?", label="search"),
        ClassifyExample(text="Discuss the intersectionality of race and LGBTQIA+ identity.", label="search"),
        ClassifyExample(text="What legal protections do LGBTQIA+ individuals have against workplace discrimination?", label="search"),
        ClassifyExample(text="How have LGBTQIA+ communities been involved in political movements?", label="search"),
        ClassifyExample(text="What are some misconceptions about the LGBTQIA+ community and how can they be addressed?", label="search"),
        ClassifyExample(text="Can you provide an overview of gender-neutral pronouns and their usage?", label="search"),
        ClassifyExample(text="What initiatives exist to support LGBTQIA+ mental health?", label="search"),
        ClassifyExample(text="Tell me about the historical significance of the Stonewall Riots.", label="search"),
        ClassifyExample(text="What's the weather like today?", label="conversation"),
        ClassifyExample(text="I'm looking for a good Italian restaurant nearby. Any suggestions?", label="conversation"),
        ClassifyExample(text="In the research paper you mentioned earlier about transgender experiences, what were the key findings?", label="conversation"),
        ClassifyExample(text="Can you tell me more about the LGBTQIA+ inclusive children's book you recommended in our previous discussion?", label="conversation"),
        ClassifyExample(text="What's your favorite color?", label="conversation"),
        ClassifyExample(text="Do you think it will rain tomorrow?", label="conversation"),
        ClassifyExample(text="Can you tell me a joke?", label="conversation"),
        ClassifyExample(text="What's the latest movie you've seen?", label="conversation"),
        ClassifyExample(text="How was your day?", label="conversation"),
        ClassifyExample(text="What do you think about the new tech gadgets?", label="conversation"),
        ClassifyExample(text="Can you recommend a good restaurant nearby?", label="conversation"),
        ClassifyExample(text="What music do you like?", label="conversation"),
        ClassifyExample(text="Have you read any good books lately?", label="conversation"),
        ClassifyExample(text="What are your hobbies?", label="conversation"),
        ClassifyExample(text="What sports do you play?", label="conversation"),
        ClassifyExample(text="Can you help me with my homework?", label="conversation"),
        ClassifyExample(text="What are some fun weekend activities?", label="conversation"),
        ClassifyExample(text="How do I fix a flat tire?", label="conversation"),
        ClassifyExample(text="What are the best vacation spots?", label="conversation"),
        ClassifyExample(text="Can you explain how to bake a cake?", label="conversation"),
        ClassifyExample(text="What are your thoughts on current events?", label="conversation"),
        ClassifyExample(text="Tell me more about your creators.", label="conversation"),
        ClassifyExample(text="What's the best way to relax after a long day?", label="conversation"),
        ClassifyExample(text="Do you have any tips for learning a new language?", label="conversation"),
        ClassifyExample(text="What are the latest trends in fashion?", label="conversation"),
        ClassifyExample(text="Can you help me plan a party?", label="conversation"),
        ClassifyExample(text="What are some effective exercise routines?", label="conversation"),
        ClassifyExample(text="How do I make a budget?", label="conversation"),
        ClassifyExample(text="What are some tips for a job interview?", label="conversation"),
        ClassifyExample(text="Can you tell me about different coffee brewing methods?", label="conversation"),
        ClassifyExample(text="What are the best apps for productivity?", label="conversation"),
        ClassifyExample(text="How do you meditate?", label="conversation"),
        ClassifyExample(text="What are some tips for taking good photos?", label="conversation"),
        ClassifyExample(text="Can you suggest some podcasts about science?", label="conversation"),
        ClassifyExample(text="What are the best strategies for online learning?", label="conversation"),
        ClassifyExample(text="How can I improve my cooking skills?", label="conversation"),
        ClassifyExample(text="What are some ways to save money?", label="conversation"),
        ClassifyExample(text="Can you explain the rules of chess?", label="conversation"),
        ClassifyExample(text="What are some DIY home improvement tips?", label="conversation"),
        ClassifyExample(text="How do I start gardening?", label="conversation"),
        ClassifyExample(text="What are the best dog breeds for apartment living?", label="conversation"),
        ClassifyExample(text="Can you guide me on how to write a resume?", label="conversation")
    ]

    # Classify the input query
    response = co.classify(
        inputs=[query],
        examples=examples
    )

    # Extract the classification label
    classification = response.classifications[0].prediction
    return classification.lower()
