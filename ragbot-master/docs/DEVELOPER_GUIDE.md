# Developer Guide

Complete guide for developers who want to contribute to or extend the O.T.T.O ChatBot project.

---

## 🎯 Overview

This guide covers:
- Development setup
- Code structure and conventions
- How to add features
- Testing procedures
- Contribution workflow

---

## 🛠️ Development Setup

### 1. Clone and Install

```bash
# Clone repository
git clone <repository-url>
cd ChatBot

# Create virtual environment
python -m venv .venv

# Activate
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

---

### 2. Project Structure

```
ChatBot/
├── main.py                 # FastAPI backend + RAG engine
├── index.html              # Frontend chat widget
├── requirements.txt        # Python dependencies
├── pyproject.toml          # UV project config
│
├── Data/
│   ├── md/                 # Source documents (markdown)
│   │   ├── Administrative & Legal/
│   │   ├── Community & Lifestyle/
│   │   └── ... (organized by category)
│   └── vectorstore/        # ChromaDB database
│
├── notebook/
│   ├── brain.ipynb         # RAG development notebook
│   └── ingest.ipynb        # Data ingestion notebook
│
└── docs/                   # Documentation
    ├── ARCHITECTURE.md
    ├── SETUP.md
    ├── MAIN_PY.md
    └── ... (all documentation)
```

---

## 📝 Code Conventions

### Python Style Guide

Follow **PEP 8** with these specifics:

**Formatting:**
- Indentation: 4 spaces
- Line length: 88 characters (Black default)
- Quotes: Double quotes for strings

**Example:**
```python
def get_answer(self, query: str) -> str:
    """
    Generate answer using RAG pipeline.
    
    Args:
        query: User's question
        
    Returns:
        AI-generated answer
    """
    if not self.vector_db:
        return "Error: Database not found."
    
    docs = self.vector_db.similarity_search(query, k=3)
    # ... rest of code
```

---

### Code Formatting

Use **Black** for automatic formatting:

```bash
# Format all Python files
black .

# Check without modifying
black --check .
```

---

### Linting

Use **flake8** for code quality:

```bash
# Run linter
flake8 main.py

# Configuration (.flake8 file)
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

---

### Type Hints

Use **mypy** for type checking:

```python
from typing import List, Optional

def search_docs(query: str, k: int = 3) -> List[str]:
    """Search and return document IDs."""
    pass

def get_llm_response(prompt: str) -> Optional[str]:
    """Get LLM response, returns None on error."""
    pass
```

Check types:
```bash
mypy main.py
```

---

## 🔧 Common Development Tasks

### Task 1: Add New Documents

**Step 1:** Add markdown file to `Data/md/`

```bash
# Example: Add new document about parking rules
echo "# Parking Rules\n\nVehicle parking is available..." > Data/md/Operations/Parking_Rules.md
```

**Step 2:** Run ingestion notebook

```bash
jupyter notebook notebook/ingest.ipynb
# Run all cells to update vector database
```

**Step 3:** Restart backend

```bash
python main.py
```

---

### Task 2: Modify Prompt Template

**File:** `main.py` (lines 59-66)

```python
# Original
prompt = f"""Use the following context to answer the question concisely 
and professionally as O.T.T.O (Smart Society Assistant).

Context:
{context}

Question: {query}

Answer:"""

# Modified (more detailed)
prompt = f"""You are O.T.T.O, a helpful Smart Society Assistant.

Instructions:
- Answer based ONLY on the context below
- Be concise and professional
- Use bullet points for lists
- If unsure, say "I don't have enough information"

Context:
{context}

Question: {query}

Answer:"""
```

---

### Task 3: Change LLM Settings

**File:** `main.py` (lines 31-36)

```python
# Original
self.llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=1024
)

# For more creative responses
self.llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,      # Higher = more creative
    max_tokens=2048       # Longer answers
)

# For faster responses (smaller model)
self.llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="mixtral-8x7b-32768",  # Faster alternative
    temperature=0.1,
    max_tokens=512
)
```

---

### Task 4: Add New API Endpoint

**Example:** Add feedback endpoint

```python
from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    rating: int  # 1-5 stars

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Store user feedback for improving responses."""
    # Save to file or database
    with open("feedback.json", "a") as f:
        f.write(f"{request.json()}\n")
    
    return {"status": "success", "message": "Thank you for your feedback!"}
```

---

### Task 5: Customize Frontend

**Change colors (index.html lines 10-15):**

```css
:root {
    --primary: #f59e0b;    /* Change to orange */
    --accent: #10b981;     /* Change to green */
    --bg-card: #1e293b;    /* Darker background */
    --text-main: #f8fafc;
}
```

**Change widget size (lines 32-35):**

```css
#chat-widget {
    width: 400px;   /* Wider */
    height: 600px;  /* Taller */
    ...
}
```

---

## 🧪 Testing

### Unit Tests

Create `test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app, RAGEngine

client = TestClient(app)

def test_greeting():
    """Test greeting response."""
    response = client.post("/ask", json={"prompt": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert "O.T.T.O" in data["answer"]
    assert data["status"] == "success"

def test_knowledge_query():
    """Test knowledge base query."""
    response = client.post("/ask", json={
        "prompt": "What facilities are available?"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_empty_prompt():
    """Test validation error for empty prompt."""
    response = client.post("/ask", json={})
    assert response.status_code == 422

def test_rag_engine():
    """Test RAGEngine initialization."""
    engine = RAGEngine()
    assert engine.embeddings is not None
    assert engine.llm is not None
    assert engine.vector_db is not None
```

**Run tests:**
```bash
pytest test_main.py -v
```

---

### Integration Tests

```python
def test_full_workflow():
    """Test complete RAG workflow."""
    response = client.post("/ask", json={
        "prompt": "What are the pool timings?"
    })
    
    data = response.json()
    assert data["status"] == "success"
    assert len(data["answer"]) > 0
    # Check for expected keywords
    assert any(word in data["answer"].lower() for word in ["pool", "time", "am", "pm"])
```

---

### Frontend Testing

**Manual testing checklist:**
- [ ] Chat trigger button opens widget
- [ ] Messages display correctly
- [ ] Markdown renders properly
- [ ] Typing indicator shows/hides
- [ ] Scroll works automatically
- [ ] Input clears after sending
- [ ] Error handling works

---

## 🔄 Git Workflow

### Branching Strategy

```bash
# Main branch
main - Production-ready code

# Development branches
develop - Integration branch
feature/feature-name - New features
bugfix/bug-name - Bug fixes
hotfix/critical-fix - Urgent production fixes
```

---

### Feature Development

```bash
# 1. Create feature branch
git checkout -b feature/add-chat-history

# 2. Make changes
# ... edit files ...

# 3. Commit changes
git add .
git commit -m "feat: Add chat history persistence"

# 4. Push to remote
git push origin feature/add-chat-history

# 5. Create Pull Request
# On GitHub/GitLab
```

---

### Commit Message Convention

Follow **Conventional Commits**:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Test additions
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(api): Add rate limiting to /ask endpoint
fix(frontend): Fix markdown rendering issue
docs: Update setup guide with Docker instructions
refactor(rag): Extract prompt template to separate file
```

---

## 📦 Adding Dependencies

### Using pip

```bash
# Install new package
pip install langchain-openai

# Update requirements.txt
pip freeze > requirements.txt
```

### Using UV

```bash
# Add dependency
uv add langchain-openai

# Remove dependency
uv remove package-name
```

---

## 🚀 Deployment

### Environment Variables

Create `.env` file:

```bash
GROQ_API_KEY=gsk_your_actual_key_here
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

Load in `main.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
```

---

### Production Configuration

**main.py modifications:**

```python
# CORS for production
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

# Run with production server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",  # Allow external access
        port=8000,
        workers=4,       # Multiple workers
        log_level="info"
    )
```

---

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
# Build image
docker build -t otto-chatbot .

# Run container
docker run -p 8000:8000 -e GROQ_API_KEY=your_key otto-chatbot
```

---

## 🐛 Debugging Tips

### Enable Debug Mode

```python
# main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True, log_level="debug")
```

---

### Add Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_answer(self, query: str):
    logger.info(f"Processing query: {query}")
    
    docs = self.vector_db.similarity_search(query, k=3)
    logger.info(f"Found {len(docs)} documents")
    
    # ... rest of code
```

---

### Frontend Debugging

```javascript
// Add console logs
console.log('Sending message:', text);
console.log('Response:', data);

// Check network in DevTools
// F12 -> Network tab -> See API calls
```

---

## 📚 Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Groq API Docs](https://console.groq.com/docs)

### Learning
- [RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with clear messages
6. **Push** to your fork
7. **Submit** a Pull Request

**PR Checklist:**
- [ ] Code follows style guide
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No sensitive data committed
- [ ] Descriptive PR title and description

---

## ❓ FAQ

**Q: How do I add a new LLM provider?**

A: Modify `RAGEngine.__init__()` to support multiple providers:

```python
def __init__(self, llm_provider="groq"):
    if llm_provider == "groq":
        self.llm = ChatGroq(...)
    elif llm_provider == "openai":
        self.llm = ChatOpenAI(...)
```

**Q: Can I use a different vector database?**

A: Yes, replace ChromaDB with Pinecone, Weaviate, or FAISS. Modify lines 39-43 in `main.py`.

**Q: How do I improve response accuracy?**

A:
1. Add more/better documents
2. Adjust chunk size in ingestion
3. Increase k in similarity search
4. Refine prompt template
5. Use a larger LLM model

---

**Next:** [API Reference](API_REFERENCE.md) | [Architecture](ARCHITECTURE.md) | [Back to README](../README.md)
