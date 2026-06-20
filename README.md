# Multi-Document AI research assitant

A sophisticated multi-document AI chatbot that processes PDF documents and answers questions using Retrieval Augmented Generation (RAG) powered by Google Generative AI and Pinecone vector database.

##  Project Overview

This project enables users to:
- **Upload PDF documents** and automatically extract and store their content
- **Ask questions** about the uploaded documents
- **Get intelligent answers** using AI with real PDF content as context
- **Track token usage** for cost monitoring and optimization

The system uses a RAG pipeline that retrieves relevant document chunks and passes them to a generative AI model for contextual, accurate responses.

##  Architecture

```
User Request
    ↓
FastAPI Server (Port 8000)
    ├── Upload PDF Handler
    │   ├── PyPDFLoader (Extract text)
    │   ├── RecursiveCharacterTextSplitter (Chunk documents)
    │   ├── GoogleGenerativeAIEmbeddings (Create embeddings)
    │   └── Pinecone (Store vectors)
    │
    └── Query Handler
        ├── Pinecone Similarity Search (Retrieve relevant chunks)
        ├── Context Assembly (Prepare prompt)
        └── ChatGoogleGenerativeAI (Generate answer)
            ↓
        Response with Token Metrics
```

## 💾 Tech Stack

### Backend Framework
- **FastAPI** (v0.138+) - Modern, fast web framework for APIs
- **Uvicorn** (v0.49+) - ASGI web server

### AI & LLM
- **Google Generative AI** (v2.9+) - Latest Google's generative AI models (Gemini)
  - Model: `gemini-2.5-flash` (or configured via env)
  - Embeddings: `gemini-embedding-2`
- **LangChain** (v1.3.10+) - LLM orchestration framework
- **LangChain Community** - Additional integrations
- **LangChain Google GenAI** - Google AI integration
- **LangChain Text Splitters** - Document chunking utilities
- **LangChain Pinecone** - Pinecone vector store integration

### Vector Database & Data Storage
- **Pinecone** (v7.3+) - Cloud-native vector database for semantic search
- **NumPy** (v2.4.6+) - Numerical computations

### Document Processing
- **PyPDF** (v6.13+) - PDF text extraction and processing
- **Python Multipart** (v0.0.32+) - Multipart form data handling (for file uploads)

### Configuration & Environment
- **Python-dotenv** (v1.2+) - Environment variable management
- **Python** (≥3.14) - Runtime

##  Project Structure

```
Multidocument-AI-Chatbot/
├── main.py                          # FastAPI app entry point
├── pyproject.toml                   # Project configuration & dependencies
├── .env                             # Environment variables (secrets)
├── .env.example                     # Example environment template
├── README.md                        # Project documentation
│
├── agentservices/                   # Core AI agent logic
│   ├── __init__.py
│   └── agentservices.py            # AgentServices class (embeddings, retrieval, LLM calls)
│
├── services/                        # Business logic layer
│   └── chatbotservices.py          # ChatbotServices class (orchestrates workflows)
│
├── controllers/                     # API endpoint handlers
│   └── botcontrollers.py           # FastAPI route definitions
│
└── models/                          # Data models & schemas
    └── pdf-request-models.py       # Request/response models
```

##  Getting Started

### Prerequisites

- Python ≥ 3.14
- `uv` package manager (or pip)
- Google API Key
- Pinecone API Key & Index

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Multidocument-AI-Chatbot
```

### 2. Set Up Environment Variables

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```env
# Google API
GOOGLE_API_KEY=your_google_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=your_pinecone_index_name

# LLM Configuration
LLM_MODEL=gemini-2.5-flash
LLM_EMbEDDING_MODEL=gemini-embedding-2

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 3. Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

### 4. Run the Server

Using `uv`:

```bash
uv run uvicorn main:app --reload --port 8080
```

Or directly:

```bash
uvicorn main:app --reload --port 8080
```

The API will be available at: `http://localhost:8080`
Interactive API docs: `http://localhost:8080/docs`

##  API Endpoints

### 1. Upload PDF Document

**Endpoint:** `POST /api/v1/bot/upload-pdf`

Upload a PDF document to be processed, chunked, embedded, and stored in Pinecone.

**Request:**
- Content-Type: `multipart/form-data`
- Body: PDF file

**Example:**
```bash
curl -X POST "http://localhost:8080/api/v1/bot/upload-pdf" \
  -F "pdf_file=@document.pdf"
```

**Response:**
```json
{
  "message": "PDF uploaded and processed successfully"
}
```

---

### 2. Ask Question About Documents

**Endpoint:** `POST /api/v1/bot/ask-question`

Ask a question about the uploaded PDF documents. The system retrieves relevant chunks and generates an answer.

**Request:**
- Query Parameter: `question` (string)

**Example:**
```bash
curl -X POST "http://localhost:8080/api/v1/bot/ask-question?question=What%20is%20the%20main%20topic%20of%20the%20document?"
```

**Response:**
```json
{
  "answer": {
    "content": "The main topic is...",
    "input_tokens": 425,
    "output_tokens": 87,
    "total_tokens": 512,
    "sources": ["document.pdf"]
  }
}
```

## 🔧 Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CHUNK_SIZE` | 1000 | Size of text chunks (characters) |
| `CHUNK_OVERLAP` | 200 | Overlap between consecutive chunks |
| `LLM_MODEL` | gemini-2.5-flash | Language model to use |
| `LLM_EMbEDDING_MODEL` | gemini-embedding-2 | Embedding model for vector generation |

## 💡 How It Works

### 1. PDF Processing & Embedding
```
PDF Upload
  ↓
Extract Text (PyPDFLoader)
  ↓
Split into Chunks (RecursiveCharacterTextSplitter)
  ↓
Generate Embeddings (GoogleGenerativeAIEmbeddings)
  ↓
Store in Vector DB (Pinecone)
```

### 2. Question Answering (RAG)
```
User Question
  ↓
Generate Query Embedding
  ↓
Semantic Search in Pinecone (retrieve top-5 relevant chunks)
  ↓
Build Context Prompt (limit to 12,000 characters)
  ↓
Send to LLM with Context
  ↓
Return Answer + Token Metrics
```

##  Token Optimization

The system includes several optimizations to reduce token consumption:

- **Limited Retrieval:** Only top 5 documents retrieved per query
- **Context Capping:** Maximum 12,000 characters of context per prompt
- **Chunk Sizing:** Configurable chunk size and overlap
- **Token Tracking:** Input/output/total tokens tracked for each response

**Monitoring:**
```python
{
  "input_tokens": 425,      # Tokens used for context + question
  "output_tokens": 87,      # Tokens generated in response
  "total_tokens": 512,      # Sum of input + output
  "sources": ["doc.pdf"]    # Source documents used
}
```

## 🧪 Testing

###  PDF Upload
```bash
curl -X POST "http://localhost:8080/api/v1/bot/upload-pdf" \
  -F "pdf_file=@test_document.pdf"
```

### Test Question Answering
```bash
curl -X POST "http://localhost:8080/api/v1/bot/ask-question?question=What%20is%20this%20document%20about?"
```

##  Troubleshooting

### Issue: `LLM request failed`
- **Solution:** Verify `GOOGLE_API_KEY` is valid and has appropriate permissions

### Issue: `Pinecone connection error`
- **Solution:** Check `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` are correct

### Issue: `No relevant documents found`
- **Solution:** Ensure PDF was successfully uploaded before asking questions

### Issue: High token consumption
- **Solution:** Reduce `CHUNK_SIZE`, `CHUNK_OVERLAP`, or adjust context capping in code

##  Future Enhancements

- [ ] Add token counting with `tiktoken` for precise token budgeting
- [ ] Implement query caching to reduce redundant API calls
- [ ] Add document summarization to compress context
- [ ] Support multiple file formats (Word, Excel, etc.)
- [ ] Add authentication and user management
- [ ] Implement streaming responses
- [ ] Add rate limiting and usage analytics
- [ ] Support multi-language documents






**Last Updated:** June 2026
**Python Version:** ≥ 3.14
**FastAPI Version:** 0.138+
