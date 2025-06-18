import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv
from utils.gemini_utils import is_gemini_configured, generate_gemini_response

# Load environment variables
load_dotenv()

# Load environment variables for Gemini API

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="MedAssist - Biofina Pharmaceuticals",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# No HuggingFace API token check needed as we're using Gemini API

# Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Custom CSS with dark mode support
def get_css():
    if st.session_state.theme == "dark":
        return """
        <style>
        /* Dark theme */
        .stApp {
            background-color: #121212;
            color: #E0E0E0;
        }
        .main-header {
            font-size: 2.5rem;
            color: #90CAF9;
            text-shadow: 0 0 10px rgba(144, 202, 249, 0.3);
        }
        .sub-header {
            font-size: 1.5rem;
            color: #64B5F6;
            text-shadow: 0 0 5px rgba(100, 181, 246, 0.3);
        }
        .chat-message {
            padding: 1.5rem; 
            border-radius: 0.5rem; 
            margin-bottom: 1rem; 
            display: flex;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .chat-message:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .chat-message.user {
            background-color: #1E1E1E;
            border-left: 3px solid #64B5F6;
        }
        .chat-message.bot {
            background-color: #2D2D2D;
            border-left: 3px solid #90CAF9;
        }
        .chat-message .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 1rem;
            border: 2px solid #64B5F6;
        }
        .chat-message .message {
            flex-grow: 1;
            padding-top: 0.2rem;
            color: #E0E0E0;
        }
        /* Sidebar styling */
        .css-1d391kg, .css-1lcbmhc, .css-12oz5g7 {
            background-color: #1E1E1E;
        }
        .stButton>button {
            background-color: #64B5F6;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #90CAF9;
            transform: scale(1.05);
        }
        /* Input field styling */
        .stTextInput>div>div>input {
            background-color: #2D2D2D;
            color: #E0E0E0;
            border: 1px solid #444;
        }
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .chat-message {
            animation: fadeIn 0.3s ease-out forwards;
        }
        </style>
        """
    else:
        return """
        <style>
        /* Light theme */
        .main-header {
            font-size: 2.5rem;
            color: #4257B2;
            text-shadow: 0 0 10px rgba(66, 87, 178, 0.1);
        }
        .sub-header {
            font-size: 1.5rem;
            color: #5C7AEA;
            text-shadow: 0 0 5px rgba(92, 122, 234, 0.1);
        }
        .chat-message {
            padding: 1.5rem; 
            border-radius: 0.5rem; 
            margin-bottom: 1rem; 
            display: flex;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .chat-message:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .chat-message.user {
            background-color: #F0F2F6;
            border-left: 3px solid #5C7AEA;
        }
        .chat-message.bot {
            background-color: #E1EBFF;
            border-left: 3px solid #4257B2;
        }
        .chat-message .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 1rem;
            border: 2px solid #5C7AEA;
        }
        .chat-message .message {
            flex-grow: 1;
            padding-top: 0.2rem;
        }
        /* Button styling */
        .stButton>button {
            background-color: #5C7AEA;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #4257B2;
            transform: scale(1.05);
        }
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .chat-message {
            animation: fadeIn 0.3s ease-out forwards;
        }
        </style>
        """

# Apply the CSS based on current theme
st.markdown(get_css(), unsafe_allow_html=True)

# Initialize session state for chat history and theme preference
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to identify relevant medication information based on query
def find_relevant_info(query, top_k=2):
    """
    Identify relevant medication information based on the user's query.
    This function analyzes the query to determine which Biofina medications might be relevant.
    
    Args:
        query: User's question
        top_k: Maximum number of relevant medications to return
        
    Returns:
        List of relevant medication information dictionaries
    """
    # Convert query to lowercase for case-insensitive matching
    query_lower = query.lower()
    
    # Define medication information with structured data
    medications = [
        {
            "title": "Biofina Pain Relief",
            "keywords": ["pain", "relief", "headache", "muscle", "ache", "fever", "acetaminophen"],
            "image_url": "https://img.freepik.com/free-vector/realistic-white-bottle-mock-up-pills_1017-17273.jpg",
            "buy_link": "https://example.com/buy/pain-relief"
        },
        {
            "title": "Biofina Allergy Relief",
            "keywords": ["allergy", "allergies", "sneezing", "runny nose", "itchy", "eyes", "loratadine", "antihistamine", "non-drowsy"],
            "image_url": "https://img.freepik.com/free-vector/realistic-white-bottle-mock-up-pills_1017-17273.jpg",
            "buy_link": "https://example.com/buy/allergy-relief"
        },
        {
            "title": "Biofina Cold & Flu",
            "keywords": ["cold", "flu", "cough", "congestion", "fever", "sore throat", "dextromethorphan", "phenylephrine"],
            "image_url": "https://img.freepik.com/free-vector/realistic-white-bottle-mock-up-pills_1017-17273.jpg",
            "buy_link": "https://example.com/buy/cold-flu"
        },
        {
            "title": "Biofina Digestive Health",
            "keywords": ["digestive", "stomach", "bloating", "gas", "bowel", "probiotic", "gut", "digestion"],
            "image_url": "https://img.freepik.com/free-vector/realistic-white-bottle-mock-up-pills_1017-17273.jpg",
            "buy_link": "https://example.com/buy/digestive-health"
        },
        {
            "title": "Biofina Sleep Aid",
            "keywords": ["sleep", "insomnia", "melatonin", "valerian", "chamomile", "rest", "drowsy", "dreams"],
            "image_url": "https://img.freepik.com/free-vector/realistic-white-bottle-mock-up-pills_1017-17273.jpg",
            "buy_link": "https://example.com/buy/sleep-aid"
        }
    ]
    
    # Score each medication based on keyword matches
    scored_meds = []
    for med in medications:
        score = 0
        title_lower = med["title"].lower()
        
        # Check for exact medication name match (highest priority)
        if med["title"].lower() in query_lower:
            score += 10
        
        # Check for partial medication name match
        title_words = title_lower.split()
        for word in title_words:
            if len(word) > 3 and word in query_lower:
                score += 5
        
        # Check for keyword matches
        for keyword in med["keywords"]:
            if keyword.lower() in query_lower:
                score += 3
        
        # General word matching with length check to avoid short common words
        for word in query_lower.split():
            if len(word) > 3:
                # Full word match with keywords
                if any(word in keyword.lower() for keyword in med["keywords"]):
                    score += 2
                # Partial word match for possible misspellings
                elif any(word[:4] in keyword.lower() for keyword in med["keywords"] if len(keyword) > 4):
                    score += 1
        
        scored_meds.append((med, score))
    
    # Sort by score (descending) and take top_k
    scored_meds.sort(key=lambda x: x[1], reverse=True)
    return [med for med, score in scored_meds[:top_k] if score > 0]

# Function to generate response
def generate_response(query, relevant_docs):
    """
    Generate a response based on the query and relevant documents.
    Uses Gemini API when available, with a simple fallback for when Gemini is not configured.
    
    Args:
        query: User's question
        relevant_docs: List of relevant documents
        
    Returns:
        Generated response
    """
    # Try to use Gemini API if configured
    if is_gemini_configured():
        try:
            # Generate response using Gemini
            return generate_gemini_response(query, relevant_docs=relevant_docs)
        except Exception as e:
            st.error(f"Error using Gemini API: {str(e)}. Falling back to simple response.")
            # Fall back to simple response if Gemini fails
    
    # Simple fallback approach when Gemini is not available
    # Check if we have any relevant documents
    if not relevant_docs:
        return (
            "I'm sorry, I don't have specific information about that in our Biofina product database. "
            "Biofina Pharmaceuticals offers medications for pain relief, allergies, cold & flu, "
            "digestive health, and sleep aid. If you're looking for information about these categories, "
            "please let me know. For all medical concerns, please consult with a healthcare professional."
        )
    
    # Extract medication names from the relevant docs
    medications = [doc["title"] for doc in relevant_docs]
    medication_list = ", ".join(medications)
    
    # Create a simple response with the relevant medications
    response = f"Based on your query, these medications might be helpful: {medication_list}\n\n"
    
    # Add information about each relevant medication
    for doc in relevant_docs:
        response += f"**{doc['title']}**\n\n"
        
        # Add image if available
        if 'image_url' in doc and doc['image_url']:
            response += f"<img src='{doc['image_url']}' width='200'/>\n\n"
        
        # Add buy link if available
        if 'buy_link' in doc and doc['buy_link']:
            response += f"<a href='{doc['buy_link']}' target='_blank'><button style='color: white; background-color: #4CAF50; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;'>Buy Now</button></a>\n\n"
    
    response += "Remember to consult with a healthcare professional before starting any new medication."
    
    return response

# This function has been removed as we now rely on Gemini for more advanced matching

# App header
st.markdown('<h1 class="main-header">MedAssist</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI Medical Assistant by Biofina Pharmaceuticals</p>', unsafe_allow_html=True)

# Sidebar with enhanced UI
with st.sidebar:
    # Logo and branding with animation
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://img.icons8.com/color/96/000000/medical-doctor.png", width=80)
    with col2:
        st.markdown("<h2 style='margin-bottom:0'>MedAssist</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top:0; color:#888;'>by Biofina Pharmaceuticals</p>", unsafe_allow_html=True)
    
    # Theme toggle with improved UI
    st.markdown("### 🎨 Appearance")
    theme_cols = st.columns([1, 1])
    with theme_cols[0]:
        light_btn_style = "primary" if st.session_state.theme == "light" else "secondary"
        if st.button("🌞 Light", type=light_btn_style, use_container_width=True):
            st.session_state.theme = "light"
            st.rerun()
    with theme_cols[1]:
        dark_btn_style = "primary" if st.session_state.theme == "dark" else "secondary"
        if st.button("🌙 Dark", type=dark_btn_style, use_container_width=True):
            st.session_state.theme = "dark"
            st.rerun()
    
    # API Status with improved UI
    st.markdown("### 🔌 API Status")
    if is_gemini_configured():
        st.success("✅ Gemini AI is active and ready")
    else:
        st.error("❌ Gemini API key not configured")
        with st.expander("How to configure Gemini"):
            st.info(
                "1. Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey)\n"
                "2. Add your key to the .env file as GEMINI_API_KEY=your_key_here\n"
                "3. Restart the application"
            )
    
    # Example questions with improved UI
    st.markdown("### 💬 Try asking about:")
    
    # Categories for example questions
    categories = {
        "Symptoms": [
            "What can help with my headache?",
            "I have allergies, what should I take?",
            "What's good for trouble sleeping?"
        ],
        "Products": [
            "Tell me about Biofina Pain Relief",
            "What are the side effects of Sleep Aid?",
            "Compare Cold & Flu and Allergy Relief"
        ],
        "Usage": [
            "Can I take Pain Relief with alcohol?",
            "How often should I take Digestive Health?",
            "Is Cold & Flu safe during pregnancy?"
        ]
    }
    
    # Display example questions by category
    category_tabs = st.tabs(list(categories.keys()))
    for i, (category, questions) in enumerate(categories.items()):
        with category_tabs[i]:
            for q in questions:
                if st.button(q, key=f"example_{q}", use_container_width=True):
                    # Add the question to the chat and process it
                    st.session_state.messages.append({"role": "user", "content": q})
                    st.rerun()
    
    # Chat controls
    st.markdown("### ⚙️ Chat Controls")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # About section
    with st.expander("ℹ️ About MedAssist"):
        st.markdown(
            "MedAssist is an AI-powered medical assistant that helps you identify potential medications "
            "from Biofina Pharmaceuticals based on your symptoms or questions. The assistant uses "
            "Google's Gemini AI to provide detailed, helpful responses."
        )
        st.warning("Always consult with a healthcare professional before starting any medication.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "© 2023 Biofina Pharmaceuticals<br>"
        "Powered by Gemini AI<br>"
        "<small>This is a demo application. Not for medical use.</small>"
        "</div>",
        unsafe_allow_html=True
    )

# Main chat container with enhanced styling
main_container = st.container()
with main_container:
    # Display chat messages with animations
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            # Add a slight delay effect between messages for visual appeal
            st.markdown(message["content"])
    
    # Chat input with enhanced UI
    if prompt := st.chat_input("Ask about symptoms or medications..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                # Find relevant information based on the query
                relevant_docs = find_relevant_info(prompt)
                
                # Generate response using Gemini or fallback
                full_response = generate_response(prompt, relevant_docs)
                
                # Simulate stream of response with milliseconds delay for better UX
                import time
                response_chunks = []
                for i in range(len(full_response) + 1):
                    # Add a typing cursor effect
                    current_response = full_response[:i] + "▌" if i < len(full_response) else full_response
                    message_placeholder.markdown(current_response)
                    
                    # Adjust typing speed based on content length for more natural feel
                    delay = 0.01 if i % 3 == 0 else 0.005
                    time.sleep(delay)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# Disclaimer with enhanced styling
st.markdown(
    "<div style='background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; "
    "border-left: 4px solid #ffc107; font-size: 0.9rem;'>"
    "<strong>Disclaimer:</strong> This chatbot is for informational purposes only and does not replace "
    "professional medical advice. Always consult with a healthcare professional for medical concerns."
    "</div>",
    unsafe_allow_html=True
)