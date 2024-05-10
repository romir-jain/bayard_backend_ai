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
    - Query: "Tell me more about the impact of LGBTQIA+ advocacy on recent legislation."
      Classification: search
    - Query: "Discuss the role of LGBTQIA+ activists in the civil rights movement."
      Classification: search
    - Query: "Can you list some influential LGBTQIA+ figures in technology?"
      Classification: search
    - Query: "What advancements have been made in LGBTQIA+ rights over the last decade?"
      Classification: search
    - Query: "Explain the significance of Pride Month and its global impact."
      Classification: search
    - Query: "What are the challenges faced by LGBTQIA+ youth in educational institutions?"
      Classification: search
    - Query: "How do different cultures view and treat LGBTQIA+ individuals?"
      Classification: search
    - Query: "Can you detail the evolution of LGBTQIA+ representation in media?"
      Classification: search
    - Query: "What are the current debates surrounding transgender athletes in sports?"
      Classification: search
    - Query: "Describe the influence of LGBTQIA+ communities on popular culture."
      Classification: search
    - Query: "What are the psychological effects of discrimination on LGBTQIA+ individuals?"
      Classification: search
    - Query: "How do LGBTQIA+ rights vary by country?"
      Classification: search
    - Query: "What support systems are available for LGBTQIA+ people facing homelessness?"
      Classification: search
    - Query: "Discuss the intersectionality of race and LGBTQIA+ identity."
      Classification: search
    - Query: "What legal protections do LGBTQIA+ individuals have against workplace discrimination?"
      Classification: search
    - Query: "How have LGBTQIA+ communities been involved in political movements?"
      Classification: search
    - Query: "What are some misconceptions about the LGBTQIA+ community and how can they be addressed?"
      Classification: search
    - Query: "Can you provide an overview of gender-neutral pronouns and their usage?"
      Classification: search
    - Query: "What initiatives exist to support LGBTQIA+ mental health?"
      Classification: search
    - Query: "Tell me about the historical significance of the Stonewall Riots."
      Classification: search
    - Query: "What's the weather like today?"
      Classification: conversation
    - Query: "I'm looking for a good Italian restaurant nearby. Any suggestions?"
      Classification: conversation
    - Query: "In the research paper you mentioned earlier about transgender experiences, what were the key findings?"
      Classification: conversation
    - Query: "Can you tell me more about the LGBTQIA+ inclusive children's book you recommended in our previous discussion?"
      Classification: conversation
    - Query: "What are some LGBTQIA+ friendly travel destinations?"
      Classification: search
    - Query: "How can workplaces be more inclusive for LGBTQIA+ employees?"
      Classification: search
    - Query: "What are the effects of LGBTQIA+ representation in children's media?"
      Classification: search
    - Query: "Can you explain the current status of LGBTQIA+ rights in Eastern Europe?"
      Classification: search
    - Query: "What are the best practices for LGBTQIA+ inclusive education?"
      Classification: search
    - Query: "How has LGBTQIA+ activism influenced public policy?"
      Classification: search
    - Query: "What are the major LGBTQIA+ advocacy groups and what do they do?"
      Classification: search
    - Query: "Discuss the impact of social media on LGBTQIA+ visibility."
      Classification: search
    - Query: "What are the common challenges LGBTQIA+ couples face in adoption?"
      Classification: search
    - Query: "How is LGBTQIA+ history taught in schools?"
      Classification: search
    - Query: "What are the trends in LGBTQIA+ representation in politics?"
      Classification: search
    - Query: "Can you provide examples of LGBTQIA+ entrepreneurship?"
      Classification: search
    - Query: "What role does religion play in the lives of many LGBTQIA+ individuals?"
      Classification: search
    - Query: "How do LGBTQIA+ issues intersect with feminism?"
      Classification: search
    - Query: "What are the global perspectives on LGBTQIA+ rights?"
      Classification: search
    - Query: "Can you detail the contributions of LGBTQIA+ individuals in science?"
      Classification: search
    - Query: "What are the ethical considerations in LGBTQIA+ research?"
      Classification: search
    - Query: "How do LGBTQIA+ issues impact mental health professionals?"
      Classification: search
    - Query: "What are the barriers to healthcare for transgender individuals?"
      Classification: search
    - Query: "Discuss the role of allyship in supporting LGBTQIA+ communities."
      Classification: search
    - Query: "What are the latest developments in LGBTQIA+ legal rights?"
      Classification: search
    - Query: "What recent legal changes have impacted the LGBTQIA+ community?"
      Classification: search
    - Query: "Can you update me on the newest legal advancements for LGBTQIA+ rights?"
      Classification: search
    - Query: "What are the current legal challenges facing the LGBTQIA+ community?"
      Classification: search
    - Query: "What recent court decisions have affected LGBTQIA+ rights?"
      Classification: search
    - Query: "How have recent legislative actions influenced LGBTQIA+ rights?"
      Classification: search
    - Query: "What are the implications of new LGBTQIA+ rights laws passed this year?"
      Classification: search
    - Query: "Discuss the impact of recent legal reforms on the LGBTQIA+ community."
      Classification: search
    - Query: "What legal protections have been extended to the LGBTQIA+ community recently?"
      Classification: search
    - Query: "Are there any upcoming legal cases concerning LGBTQIA+ rights?"
      Classification: search
    - Query: "How do recent legal decisions impact transgender rights specifically?"
      Classification: search
    - Query: "What progress has been made in LGBTQIA+ rights in conservative regions?"
      Classification: search
    - Query: "What setbacks have LGBTQIA+ rights faced in the legal system recently?"
      Classification: search
    - Query: "Can you provide a summary of this year's legal advancements for LGBTQIA+ rights?"
      Classification: search
    - Query: "What are the most controversial legal issues currently affecting the LGBTQIA+ community?"
      Classification: search
    - Query: "Discuss the role of advocacy groups in recent LGBTQIA+ legal victories."
      Classification: search
    - Query: "What are the key legal battles that the LGBTQIA+ community is currently facing?"
      Classification: search
    - Query: "How have international laws affecting LGBTQIA+ rights evolved recently?"
      Classification: search
    - Query: "What legal strategies are being used to combat discrimination against LGBTQIA+ individuals?"
      Classification: search
    - Query: "Discuss the effectiveness of recent legal changes in protecting LGBTQIA+ youth."
      Classification: search
    - Query: "What are the latest legal discussions around LGBTQIA+ rights in the workplace?"
      Classification: search
    - Query: "How are LGBTQIA+ legal rights being addressed in educational institutions?"
      Classification: search
    - Query: "What new legal precedents have been set for LGBTQIA+ rights?"
      Classification: search
    - Query: "Discuss the intersection of LGBTQIA+ rights with other civil rights movements in recent legal developments."
      Classification: search
    - Query: "What are the challenges in enforcing new LGBTQIA+ rights laws?"
      Classification: search
    - Query: "How are LGBTQIA+ rights being impacted by changes in government administrations?"
      Classification: search
    - Query: "What are the debates surrounding privacy and LGBTQIA+ rights in the legal sphere?"
      Classification: search
    - Query: "Discuss the global trends in legal protections for LGBTQIA+ individuals."
      Classification: search
    - Query: "What are the legal implications of recent hate crimes against the LGBTQIA+ community?"
      Classification: search
    - Query: "How is the legal system addressing marriage equality for LGBTQIA+ couples?"
      Classification: search
    - Query: "What are the legal challenges faced by LGBTQIA+ immigrants?"
      Classification: search
    - Query: "Discuss the role of the judiciary in shaping LGBTQIA+ rights."
      Classification: search
    - Query: "What are the legal outcomes of recent LGBTQIA+ discrimination lawsuits?"
      Classification: search
    - Query: "How are LGBTQIA+ rights being influenced by public opinion and legal actions?"
      Classification: search
    - Query: "What are the latest legal guidelines for LGBTQIA+ rights in healthcare?"
      Classification: search
    - Query: "Discuss the impact of legal advocacy on LGBTQIA+ rights advancements."
      Classification: search
    - Query: "What are the emerging legal issues for LGBTQIA+ communities in rural areas?"
      Classification: search
    - Query: "How are LGBTQIA+ rights being integrated into existing civil rights laws?"
      Classification: search
    - Query: "What are the legal perspectives on LGBTQIA+ adoption rights?"
      Classification: search
    - Query: "Discuss the legal ramifications of anti-LGBTQIA+ legislation."
      Classification: search
    - Query: "What are the legal considerations for LGBTQIA+ individuals in the military?"
      Classification: search
    - Query: "How are LGBTQIA+ rights being addressed in international human rights law?"
      Classification: search
    - Query: "What are the legal challenges and successes in LGBTQIA+ elder rights?"
      Classification: search
    - Query: "Discuss the legal landscape for LGBTQIA+ rights in emerging economies."
      Classification: search
    - Query: "What are the legal barriers to LGBTQIA+ equality in sports?"
      Classification: search
    - Query: "How is the legal framework evolving to protect LGBTQIA+ individuals from violence?"
      Classification: search
    - Query: "What are the legal strategies for advancing LGBTQIA+ rights in conservative legal systems?"
      Classification: search
    - Query: "Discuss the legal protections for LGBTQIA+ individuals in the tech industry."
      Classification: search
    - Query: "What are the legal implications of recent LGBTQIA+ rights protests?"
      Classification: search
    - Query: "How are LGBTQIA+ rights being negotiated in religious contexts?"
      Classification: search
    - Query: "What's your favorite color?"
      Classification: conversation
    - Query: "Do you think it will rain tomorrow?"
      Classification: conversation
    - Query: "Can you tell me a joke?"
      Classification: conversation
    - Query: "What's the latest movie you've seen?"
      Classification: conversation
    - Query: "How was your day?"
      Classification: conversation
    - Query: "What do you think about the new tech gadgets?"
      Classification: conversation
    - Query: "Can you recommend a good restaurant nearby?"
      Classification: conversation
    - Query: "What music do you like?"
      Classification: conversation
    - Query: "Have you read any good books lately?"
      Classification: conversation
    - Query: "What are your hobbies?"
      Classification: conversation
    - Query: "What sports do you play?"
      Classification: conversation
    - Query: "Can you help me with my homework?"
      Classification: conversation
    - Query: "What are some fun weekend activities?"
      Classification: conversation
    - Query: "How do I fix a flat tire?"
      Classification: conversation
    - Query: "What are the best vacation spots?"
      Classification: conversation
    - Query: "Can you explain how to bake a cake?"
      Classification: conversation
    - Query: "What are your thoughts on current events?"
      Classification: conversation
    - Query: "Tell me more about your creators."
      Classification: conversation
    - Query: "What's the best way to relax after a long day?"
      Classification: conversation
    - Query: "Do you have any tips for learning a new language?"
      Classification: conversation
    - Query: "What are the latest trends in fashion?"
      Classification: conversation
    - Query: "Can you help me plan a party?"
      Classification: conversation
    - Query: "What are some effective exercise routines?"
      Classification: conversation
    - Query: "How do I make a budget?"
      Classification: conversation
    - Query: "What are some tips for a job interview?"
      Classification: conversation
    - Query: "Can you tell me about different coffee brewing methods?"
      Classification: conversation
    - Query: "What are the best apps for productivity?"
      Classification: conversation
    - Query: "How do you meditate?"
      Classification: conversation
    - Query: "What are some tips for taking good photos?"
      Classification: conversation
    - Query: "Can you suggest some podcasts about science?"
      Classification: conversation
    - Query: "What are the best strategies for online learning?"
      Classification: conversation
    - Query: "How can I improve my cooking skills?"
      Classification: conversation
    - Query: "What are some ways to save money?"
      Classification: conversation
    - Query: "Can you explain the rules of chess?"
      Classification: conversation
    - Query: "What are some DIY home improvement tips?"
      Classification: conversation
    - Query: "How do I start gardening?"
      Classification: conversation
    - Query: "What are the best dog breeds for apartment living?"
      Classification: conversation
    - Query: "Can you guide me on how to write a resume?"


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