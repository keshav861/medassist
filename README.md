# MedAssist Chatbot

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-blue)](https://biofina.streamlit.app/)
[![GitHub](https://img.shields.io/github/license/keshav861/medassist)](https://github.com/keshav861/medassist/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

</div>

## 📋 Overview

MedAssist is an intelligent medical assistant chatbot designed to help users identify potential medications from Biofina Pharmaceuticals based on their symptoms. The chatbot leverages RAG (Retrieval Augmented Generation) with HuggingFace's Inference API to provide accurate information and recommendations without requiring local model downloads.

🔗 **Live Demo**: [https://biofina.streamlit.app/](https://biofina.streamlit.app/)

## ✨ Features

- 🔍 Intelligent symptom-based medication recommendations
- 💊 Comprehensive information about Biofina Pharmaceuticals products
- 🌐 User-friendly interface built with Streamlit
- 🤖 Advanced RAG (Retrieval Augmented Generation) system
- ⚡ Fast responses using HuggingFace's Inference API
- 🔒 Privacy-focused design with no data storage
- ⚕️ Professional medical disclaimer and guidance

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/keshav861/medassist.git
   cd medassist
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up environment variables
   - Create a `.env` file in the root directory
   - Add your HuggingFace API token for higher rate limits:
     ```env
     HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
     ```
   - Get your free API token at [HuggingFace](https://huggingface.co/)

4. Launch the application
   ```bash
   streamlit run app.py
   ```

## 🏗️ Project Structure

```
medassist/
├── app.py              # Main Streamlit application
├── data/              # Medical knowledge base and product information
├── utils/             # Utility functions
│   ├── __init__.py
│   ├── data_utils.py   # Data loading and processing
│   ├── gemini_utils.py # Gemini model integration
│   ├── prompt_utils.py # Prompt templates
│   └── rag_utils.py    # Vector store and retrieval functions
├── requirements.txt    # Required Python packages
├── setup.py           # Setup script
└── README.md          # Project documentation
```

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI/ML**: 
  - HuggingFace Inference API
  - RAG (Retrieval Augmented Generation)
  - Vector Embeddings
- **Data Processing**: Python with pandas and numpy
- **Deployment**: Streamlit Cloud

## 💡 How It Works

1. User inputs their symptoms through the chat interface
2. The RAG system retrieves relevant medical information from the knowledge base
3. HuggingFace's Inference API processes the input and generates recommendations
4. The system provides medication suggestions from Biofina Pharmaceuticals
5. Users receive comprehensive information about recommended products

## ⚠️ Disclaimer

This chatbot is for informational purposes only and does not replace professional medical advice. Always consult with a qualified healthcare professional for medical concerns and before starting any medication.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 🙋‍♂️ Author

**Keshav**
- GitHub: [@keshav861](https://github.com/keshav861)

## 🙏 Acknowledgments

- Thanks to HuggingFace for providing the Inference API
- Streamlit team for the excellent web framework
- Biofina Pharmaceuticals for the medical product information