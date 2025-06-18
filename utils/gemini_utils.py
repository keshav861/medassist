import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# Load environment variables
load_dotenv()

# Configure the Gemini API with the key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "your_gemini_api_key_here":
    genai.configure(api_key=api_key)

# Default model to use
DEFAULT_MODEL = "gemini-1.5-flash"

# Check if Gemini API is configured
def is_gemini_configured() -> bool:
    """
    Check if the Gemini API is properly configured with a valid API key.
    
    Returns:
        bool: True if configured, False otherwise
    """
    return api_key is not None and api_key != "your_gemini_api_key_here"

# Initialize the Gemini model
def get_gemini_model(model_name: str = DEFAULT_MODEL):
    """
    Get a Gemini model instance.
    
    Args:
        model_name: Name of the Gemini model to use
        
    Returns:
        GenerativeModel: The Gemini model instance
    """
    if not is_gemini_configured():
        raise ValueError("Gemini API key not configured. Please add your API key to the .env file.")
    
    return genai.GenerativeModel(model_name)

# Format system prompt for medical assistant
def format_system_prompt() -> str:
    """
    Format a system prompt for the Gemini model with information about Biofina Pharmaceuticals.
    
    Returns:
        str: Formatted system prompt
    """
    return (
        "You are MedAssist, an AI medical assistant created by Biofina Pharmaceuticals. "
        "Your purpose is to provide helpful information about symptoms and suggest appropriate "
        "Biofina medications that might help with those symptoms. Be empathetic, professional, and detailed. "
        "\n\nBiofina Pharmaceuticals offers the following medications:\n"
        "1. Biofina Pain Relief - for headaches, muscle aches, and fever reduction. Contains acetaminophen. "
        "Side effects may include nausea and drowsiness. Not recommended for liver conditions.\n"
        "2. Biofina Allergy Relief - for seasonal allergies, providing 24-hour relief from sneezing, runny nose, and itchy eyes. "
        "Contains loratadine, a non-drowsy formula. Side effects may include dry mouth and headache.\n"
        "3. Biofina Cold & Flu - for symptom relief of common cold and influenza. Contains acetaminophen, dextromethorphan, and phenylephrine. "
        "May cause drowsiness. Not recommended for high blood pressure.\n"
        "4. Biofina Digestive Health - a probiotic supplement supporting gut health and digestion. "
        "Contains beneficial bacteria including Lactobacillus and Bifidobacterium strains. Helps with bloating and gas.\n"
        "5. Biofina Sleep Aid - a non-habit forming sleep supplement with melatonin, valerian root, and chamomile. "
        "Helps reduce time to fall asleep. May cause vivid dreams. Not for pregnant women.\n\n"
        "When responding to users, provide detailed information about these medications based on their symptoms or questions. "
        "Include dosage information, side effects, and contraindications when relevant. "
        "Always remind users to consult healthcare professionals before starting any medication."
    )

# Generate response using Gemini
def generate_gemini_response(
    query: str, 
    medical_data: List[Dict[str, Any]] = None, 
    relevant_docs: List[Dict[str, Any]] = None,
    model_name: str = DEFAULT_MODEL
) -> str:
    """
    Generate a response using the Gemini model.
    
    Args:
        query: User's question
        medical_data: List of all medication data dictionaries (optional, for backward compatibility)
        relevant_docs: List of relevant medication documents (optional)
        model_name: Name of the Gemini model to use
        
    Returns:
        str: Generated response
    """
    try:
        if not is_gemini_configured():
            raise ValueError("Gemini API key not configured")
        
        # Get the model
        model = get_gemini_model(model_name)
        
        # Create system prompt
        system_prompt = format_system_prompt()
        
        # Prepare context information if relevant docs are provided
        context = ""
        if relevant_docs and len(relevant_docs) > 0:
            context = "Based on your question, these medications might be relevant:\n\n"
            for doc in relevant_docs:
                # Include all available information including image and buy link if available
                context += f"- {doc['title']}\n"
                
                if 'image_url' in doc and doc['image_url']:
                    context += f"  Image available at: {doc['image_url']}\n"
                    
                if 'buy_link' in doc and doc['buy_link']:
                    context += f"  Purchase link: {doc['buy_link']}\n"
                    
                context += "\n"
            
            context += "Please provide detailed information about these medications in your response. "
            context += "If appropriate, include the image URLs and purchase links in your response using HTML.\n"
        
        # Configure the model with the system prompt
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        # Prepare the prompt with context
        prompt_parts = [
            system_prompt,
            "\n\n",
            context,
            "\n\nUser Question: ",
            query,
            "\n\nPlease format your response in markdown. If relevant, include HTML for images and 'Buy Now' buttons. Make your response visually appealing."
        ]
        
        # Generate response
        response = model.generate_content(
            prompt_parts,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Format the response
        formatted_response = response.text
        
        # Add disclaimer if not already included
        if "consult with a healthcare professional" not in formatted_response.lower():
            formatted_response += "\n\n*Remember to consult with a healthcare professional before starting any new medication.*"
        
        return formatted_response
        
    except Exception as e:
        # Fallback response in case of API errors
        error_message = str(e)
        return (
            f"I apologize, but I encountered an error while generating a response: {error_message}\n\n"
            "Please try again later or contact support if the issue persists. "
            "In the meantime, you can ask about Biofina medications such as Pain Relief, Allergy Relief, "
            "Cold & Flu, Digestive Health, or Sleep Aid."
        )