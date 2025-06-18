# MedAssist Chatbot

A medical assistant chatbot that helps users identify potential medications from Biofina Pharmaceuticals based on their symptoms. The chatbot uses RAG (Retrieval Augmented Generation) with HuggingFace's Inference API to provide accurate information and recommendations without requiring local model downloads.

## Features

- Symptom-based medication recommendations
- Information about Biofina Pharmaceuticals products
- User-friendly interface built with Streamlit
- Reminder to consult with healthcare professionals

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. (Optional) Create a `.env` file with your HuggingFace API token for higher rate limits:
   ```
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
   ```
   You can get a free API token by creating an account at [HuggingFace](https://huggingface.co/)
4. Run the application:
   ```
   streamlit run app.py
   ```
   
   The application uses HuggingFace's Inference API, so no models are downloaded to your local system.

## Project Structure

- `app.py`: Main Streamlit application
- `data/`: Contains medical knowledge base and product information
- `utils/`: Utility functions for RAG implementation
  - `hf_utils.py`: HuggingFace Inference API integration for models and embeddings
  - `rag_utils.py`: Vector store and retrieval functions
  - `data_utils.py`: Data loading and processing
  - `prompt_utils.py`: Prompt templates
- `requirements.txt`: Required Python packages
- `setup.py`: Setup script for the application
- `.env.example`: Example environment variables configuration

## Disclaimer

This chatbot is for informational purposes only and does not replace professional medical advice. Always consult with a healthcare professional for medical concerns.