# Sociology Tutor - AI Microservice

FastAPI-based RAG (Retrieval-Augmented Generation) microservice that powers the Sociology Tutor application.

## 🧠 Tech Stack

- **FastAPI** - Web framework
- **LangChain** - RAG orchestration
- **Ollama** - Local LLM inference (Mistral)
- **ChromaDB** - Vector database
- **OpenStax Sociology Textbook** - Knowledge base

## 🚀 Setup

### Prerequisites
- Python 3.9+
- Ollama installed locally

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
```

The service will start on `http://127.0.0.1:8000`

## 📡 API Endpoints

- `POST /ask` - Ask a question about sociology
- `POST /summarize` - Generate a summary of chat history
- `GET /health` - Health check

## 🔗 Related Repositories

- [soc-tutor-app](https://github.com/Kristin611/soc-tutor-app) - Frontend and Backend