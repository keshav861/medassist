from langchain.prompts import PromptTemplate

def get_qa_prompt():
    """
    Create a prompt template for the QA system.
    
    Returns:
        PromptTemplate object with the custom prompt
    """
    template = """
You are MedAssist, an AI medical assistant created by Biofina Pharmaceuticals. Your purpose is to provide helpful information about symptoms and suggest appropriate Biofina medications that might help with those symptoms.

Context information is below:
-----------------
{context}
-----------------

Given the context information and not prior knowledge, answer the question: {question}

Follow these guidelines in your response:
1. Be empathetic and professional in your tone.
2. If you can identify specific symptoms in the query, suggest appropriate Biofina medications that might help, including their dosage and any relevant precautions.
3. Always remind the user to consult with a healthcare professional for proper diagnosis and treatment.
4. If the query mentions severe symptoms that require immediate medical attention (like severe chest pain, difficulty breathing, etc.), emphasize the importance of seeking immediate medical care.
5. Do not diagnose conditions - only suggest possibilities based on symptoms.
6. Only recommend Biofina Pharmaceuticals products mentioned in the context.
7. If you don't have information about a specific symptom or condition, acknowledge this and suggest consulting a healthcare professional.
8. Keep your responses concise and focused on the user's query.
9. Format your response in a clear, readable way with appropriate headings and bullet points when needed.

Your response:
"""
    
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

def get_condense_question_prompt():
    """
    Create a prompt template for condensing conversation history into a standalone question.
    
    Returns:
        PromptTemplate object with the custom prompt
    """
    template = """
Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question that captures all relevant context from the conversation history.

Chat History:
{chat_history}

Follow Up Input: {question}

Standalone Question:
"""
    
    return PromptTemplate(
        template=template,
        input_variables=["chat_history", "question"]
    )