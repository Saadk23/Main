# main.py - Backend Documentation

Complete guide to understanding the FastAPI backend and RAG engine implementation.

---

## 📄 File Overview

**File:** `main.py`  
**Purpose:** FastAPI backend server with RAG (Retrieval Augmented Generation) engine  
**Lines of Code:** 95  
**Key Components:**
- FastAPI application with CORS
- RAGEngine class (embeddings + vector DB + LLM)
- `/ask` endpoint for chat queries

---

## 🏗️ Code Structure

```python
Imports (lines 1-7)
    ↓
FastAPI App + CORS Setup (lines 9-17)
    ↓
Constants Configuration (lines 19-23)
    ↓
RAGEngine Class (lines 25-69)
    ├── __init__() - Initialize components
    └── get_answer() - RAG pipeline
    ↓
Engine Instance (line 72)
    ↓
Pydantic Models (lines 74-75)
    ↓
API Endpoint (lines 77-91)
    └── @app.post("/ask")
    ↓
Main Entry Point (lines 93-95)
```

---

## 📦 Imports Explained

### Line 1-6: Core Dependencies

```python
from fastapi import FastAPI                    # Web framework
from fastapi.middleware.cors import CORSMiddleware  # Cross-origin requests
from pydantic import BaseModel                 # Request validation
import os                                      # File path handling
from langchain_chroma import Chroma           # Vector database
from langchain_huggingface import HuggingFaceEmbeddings  # Text embeddings
from langchain_groq import ChatGroq           # LLM integration
```

**Why these libraries?**
- **FastAPI**: Modern, fast, async Python web framework
- **Pydantic**: Type validation for request/response
- **LangChain**: Abstractions for RAG workflow
- **ChromaDB**: Embedded vector database
- **HuggingFace**: Pre-trained embedding models
- **Groq**: Fast LLM inference API

---

## ⚙️ Configuration (Lines 19-23)

```python
MODEL_NAME = "all-MiniLM-L6-v2"                        # Embedding model
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Project root
VECTOR_DB_PATH = os.path.join(BASE_DIR, "Data", "vectorstore")  # DB path
GROQ_API_KEY = "gsk_..."                               # API key
```

### Configuration Details

| Constant | Value | Purpose |
|----------|-------|---------|
| `MODEL_NAME` | all-MiniLM-L6-v2 | 384-dim sentence embeddings |
| `BASE_DIR` | Script directory | Resolves relative paths |
| `VECTOR_DB_PATH` | Data/vectorstore | Location of ChromaDB |
| `GROQ_API_KEY` | API key string | Authentication for LLM |

**⚠️ Security Note:** API key should be in environment variables!

**Better approach:**
```python
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "fallback_key")
```

---

## 🚀 FastAPI Application (Lines 9-17)

```python
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all headers
)
```

### CORS Configuration

**Current Setting:** `allow_origins=["*"]` - Allows requests from any domain

**Why needed?** 
- Frontend (index.html) runs on different port/domain
- Browser enforces same-origin policy
- CORS headers permit cross-origin requests

**Production Recommendation:**
```python
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

---

## 🧠 RAGEngine Class (Lines 25-69)

### Class Purpose
Orchestrates the RAG (Retrieval Augmented Generation) workflow:
1. Load embeddings model
2. Initialize LLM
3. Connect to vector database
4. Process queries with context retrieval

---

### `__init__()` Method (Lines 26-45)

```python
def __init__(self):
    # 1. Load embedding model
    self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    
    # 2. Initialize Groq LLM
    self.llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,      # Low = more deterministic
        max_tokens=1024       # Response length limit
    )
    
    # 3. Load vector database
    if os.path.exists(VECTOR_DB_PATH):
        self.vector_db = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=self.embeddings
        )
    else:
        self.vector_db = None
```

#### Initialization Steps

**Step 1: Embeddings (Line 28)**
- Model: `all-MiniLM-L6-v2` (sentence-transformers)
- Dimensions: 384
- Purpose: Convert text to vectors
- Download: Cached in `~/.cache/huggingface/`

**Step 2: LLM (Lines 31-36)**
- Provider: Groq
- Model: Llama 3.3 70B (versatile variant)
- Temperature: 0.1 (range: 0.0-1.0)
  - Low temp = consistent, factual
  - High temp = creative, varied
- Max tokens: 1024 (approx 750 words)

**Step 3: Vector DB (Lines 39-45)**
- Checks if database exists
- Loads from `persist_directory`
- Uses same embedding function for queries
- If missing, sets `self.vector_db = None`

---

### `get_answer()` Method (Lines 47-69)

**Main RAG workflow method**

```python
def get_answer(self, query: str):
    # 1. Validate database
    if not self.vector_db:
        return "Error: Database not found."
    
    # 2. Retrieve relevant documents (Retrieval)
    docs = self.vector_db.similarity_search(query, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    # 3. Check if context found
    if not context:
        return "No relevant context found to answer."
    
    # 4. Create prompt with context (Augmented)
    prompt = f"""Use the following context to answer the question...
    Context: {context}
    Question: {query}
    Answer:"""
    
    # 5. Generate answer (Generation)
    response = self.llm.invoke([prompt])
    return response.content
```

#### Method Flow Breakdown

**Step 1: Validation (Lines 48-49)**
```python
if not self.vector_db:
    return "Error: Database not found."
```
- Ensures vector database is loaded
- Early return if missing

**Step 2: Document Retrieval (Lines 51-53)**
```python
docs = self.vector_db.similarity_search(query, k=3)
context = "\n\n".join([d.page_content for d in docs])
```
- `similarity_search()`: Finds top-k most similar documents
- `k=3`: Returns 3 most relevant chunks
- Concatenates document content with double newlines
- Uses cosine similarity on embedding vectors

**Step 3: Context Check (Lines 55-56)**
```python
if not context:
    return "No relevant context found to answer."
```
- Handles edge case of no matches
- Should rarely happen with large corpus

**Step 4: Prompt Construction (Lines 58-66)**
```python
prompt = f"""Use the following context to answer the question concisely 
and professionally as O.T.T.O (Smart Society Assistant).

Context:
{context}

Question: {query}

Answer:"""
```
- Template instructs LLM behavior
- Provides retrieved context
- Adds user query
- Requests role-play as O.T.T.O

**Step 5: LLM Generation (Lines 68-69)**
```python
response = self.llm.invoke([prompt])
return response.content
```
- Sends prompt to Groq API
- `invoke()`: Synchronous call
- Returns only the text content

---

## 🌐 API Endpoint (Lines 77-91)

### Request Model (Lines 74-75)

```python
class ChatRequest(BaseModel):
    prompt: str
```

Pydantic model for type validation:
- Expects JSON: `{"prompt": "user question"}`
- Validates `prompt` is a string
- Auto-generates OpenAPI schema

---

### POST /ask Endpoint (Lines 77-91)

```python
@app.post("/ask")
async def ask_bot(request: ChatRequest):
    user_prompt = request.prompt.lower().strip()
    
    # Simple greetings handler
    greetings = ["hello", "hi", "salam", "hey"]
    if any(g in user_prompt for g in greetings):
        return {
            "answer": "Hello! I am O.T.T.O. How can I assist you...",
            "status": "success"
        }
    
    try:
        # RAG workflow
        final_answer = engine.get_answer(request.prompt)
        return {"answer": final_answer, "status": "success"}
    except Exception as e:
        return {"answer": f"System Error: {str(e)}", "status": "error"}
```

#### Endpoint Logic

**1. Input Processing (Line 79)**
```python
user_prompt = request.prompt.lower().strip()
```
- Converts to lowercase for comparison
- Removes leading/trailing whitespace

**2. Greeting Detection (Lines 82-84)**
```python
greetings = ["hello", "hi", "salam", "hey"]
if any(g in user_prompt for g in greetings):
    return {...}
```
- Fast response for simple greetings
- Avoids unnecessary LLM call
- Supports multilingual greetings

**3. RAG Processing (Lines 86-89)**
```python
try:
    final_answer = engine.get_answer(request.prompt)
    return {"answer": final_answer, "status": "success"}
```
- Calls RAG engine
- Uses original prompt (not lowercased)
- Returns JSON response

**4. Error Handling (Lines 90-91)**
```python
except Exception as e:
    return {"answer": f"System Error: {str(e)}", "status": "error"}
```
- Catches all exceptions
- Returns error message to user
- Prevents server crash

---

## 🎯 Global Engine Instance (Line 72)

```python
engine = RAGEngine()
```

**Singleton pattern:**
- Creates ONE instance when server starts
- Reused for all requests
- Avoids reloading models on each request
- Memory efficient

**Alternative (not used):**
```python
# Create new instance per request (wasteful!)
@app.post("/ask")
async def ask_bot(request: ChatRequest):
    engine = RAGEngine()  # Don't do this!
```

---

## 🚀 Server Entry Point (Lines 93-95)

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Uvicorn Configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `app` | FastAPI instance | ASGI application |
| `host` | 127.0.0.1 | Localhost only |
| `port` | 8000 | HTTP port |

**Start server:**
```bash
python main.py
```

**Alternative production config:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🔄 Request/Response Examples

### Example 1: Greeting

**Request:**
```json
POST /ask
{
  "prompt": "Hello"
}
```

**Response:**
```json
{
  "answer": "Hello! I am O.T.T.O. How can I assist you with society matters today?",
  "status": "success"
}
```

---

### Example 2: Knowledge Query

**Request:**
```json
POST /ask
{
  "prompt": "What are the swimming pool timings?"
}
```

**Internal Flow:**
1. Embedding: `"What are the swimming pool timings?"` → [0.1, -0.3, ...]
2. Search: Find top 3 similar documents
3. Context: Retrieved text about pool facilities
4. LLM: Generate answer from context
5. Response: Formatted answer

**Response:**
```json
{
  "answer": "The swimming pool is open from 6:00 AM to 10:00 PM daily. Please note that...",
  "status": "success"
}
```

---

### Example 3: Error Case

**Request:**
```json
POST /ask
{
  "prompt": "Test query"
}
```

**If database missing:**
```json
{
  "answer": "Error: Database not found.",
  "status": "success"
}
```

**If LLM fails:**
```json
{
  "answer": "System Error: API key invalid",
  "status": "error"
}
```

---

## 🔧 Customization Guide

### Change Embedding Model

```python
# Line 20
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

### Adjust LLM Parameters

```python
# Lines 31-36
self.llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",  # or "mixtral-8x7b-32768"
    temperature=0.3,     # Increase for more creativity
    max_tokens=2048      # Increase for longer answers
)
```

### Change Search Results Count

```python
# Line 52
docs = self.vector_db.similarity_search(query, k=5)  # Get 5 documents
```

### Add Authentication

```python
from fastapi import Header, HTTPException

@app.post("/ask")
async def ask_bot(request: ChatRequest, api_key: str = Header(...)):
    if api_key != "your_secret_key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    # ... rest of code
```

---

## 🧪 Testing the Backend

### Manual Testing

```bash
# Start server
python main.py

# In another terminal, test with curl
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

### Using FastAPI Docs

1. Start server
2. Visit: `http://127.0.0.1:8000/docs`
3. Expand `/ask` endpoint
4. Click "Try it out"
5. Enter test prompt
6. Click "Execute"

---

## 🐛 Common Issues & Solutions

### Issue: "Database not found"
**Cause:** Vector database doesn't exist  
**Solution:** Run `notebook/ingest.ipynb`

### Issue: Slow responses
**Cause:** Large k value or slow internet  
**Solution:** Reduce k parameter or optimize context

### Issue: "Connection refused"
**Cause:** Server not running  
**Solution:** Start with `python main.py`

### Issue: CORS errors
**Cause:** Missing CORS middleware  
**Solution:** Verify lines 12-17 are present

---

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Groq API Docs](https://console.groq.com/docs)
- [ChromaDB Guide](https://docs.trychroma.com/)

---

**Next:** [Frontend Documentation](INDEX_HTML.md) | [API Reference](API_REFERENCE.md) | [Back to README](../README.md)
