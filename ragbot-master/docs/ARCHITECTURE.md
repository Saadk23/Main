# System Architecture

This document explains the technical architecture of the O.T.T.O Smart Society Assistant ChatBot.

---

## 🏛️ High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                         │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          index.html (Web Chat Widget)                 │   │
│  │  • Modern UI with glassmorphism design                │   │
│  │  • Real-time message display                          │   │
│  │  • Markdown rendering support                         │   │
│  └────────────────────┬─────────────────────────────────┘   │
└─────────────────────────┼──────────────────────────────────────┘
                          │ HTTP POST /ask
                          │ JSON: {prompt: "..."}
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                          │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   main.py                             │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │         @app.post("/ask")                    │    │   │
│  │  │  • Handles user queries                      │    │   │
│  │  │  • Greeting detection                        │    │   │
│  │  │  • Error handling                            │    │   │
│  │  └──────────────┬──────────────────────────────┘    │   │
│  │                 │                                     │   │
│  │                 ▼                                     │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │         RAGEngine Class                      │    │   │
│  │  │  • Orchestrates RAG workflow                 │    │   │
│  │  │  • Manages embeddings & LLM                  │    │   │
│  │  └──────────────┬──────────────────────────────┘    │   │
│  └─────────────────┼──────────────────────────────────┘   │
└────────────────────┼───────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│   VECTOR DB     │    │    LLM SERVICE   │
│                 │    │                  │
│  ChromaDB       │    │   Groq API       │
│  • Embeddings   │    │   • Llama 3.3    │
│  • Similarity   │    │   • 70B params   │
│    Search       │    │   • Low temp     │
└─────────────────┘    └──────────────────┘
```

---

## 🔄 Request Flow (RAG Pipeline)

### Step-by-Step Flow

```
1. USER INPUT
   ↓
   User types: "What are the pool timings?"
   
2. FRONTEND (index.html)
   ↓
   • sendMessage() captures input
   • Displays user message in chat
   • Shows "O.T.T.O is typing..." indicator
   • Makes POST request to http://127.0.0.1:8000/ask
   
3. BACKEND ROUTING (FastAPI)
   ↓
   • @app.post("/ask") receives request
   • Extracts prompt from JSON body
   • Checks for simple greetings
   • Forwards to RAGEngine.get_answer()
   
4. RETRIEVAL PHASE
   ↓
   RAGEngine.get_answer():
   • Converts query to embedding vector (384 dimensions)
   • Performs similarity search in ChromaDB
   • Retrieves top 3 most relevant documents
   • Concatenates document content as context
   
5. GENERATION PHASE
   ↓
   • Creates prompt template with context + query
   • Sends to Groq API (Llama 3.3 70B)
   • LLM generates answer based on context
   • Temperature: 0.1 (more deterministic)
   • Max tokens: 1024
   
6. RESPONSE
   ↓
   • Backend returns JSON: {answer: "...", status: "success"}
   • Frontend receives response
   • Hides typing indicator
   • Renders answer with markdown support
   • Scrolls chat to bottom
```

---

## 🧩 Component Details

### 1. Frontend (index.html)

**Responsibilities:**
- User interface rendering
- Message display and formatting
- API communication
- Markdown parsing

**Key Technologies:**
- Vanilla JavaScript (no frameworks)
- marked.js for Markdown rendering
- CSS3 with custom properties
- Fetch API for HTTP requests

**Design Features:**
- Glassmorphism effects
- Smooth animations
- Responsive layout
- Dark mode theme

---

### 2. Backend API (main.py)

#### FastAPI Application

```python
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

**Features:**
- Cross-Origin Resource Sharing (CORS) enabled
- Async request handling
- JSON request/response
- Error handling with try/catch

#### RAGEngine Class

**Initialization:**
```python
def __init__(self):
    self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    self.llm = ChatGroq(...)
    self.vector_db = Chroma(...)
```

**Key Methods:**
- `get_answer(query: str)` - Main RAG workflow
  1. Similarity search
  2. Context extraction
  3. Prompt construction
  4. LLM invocation

---

### 3. Vector Database (ChromaDB)

**Purpose:** Semantic search over society documents

**Structure:**
```
Data/vectorstore/
├── chroma.sqlite3              # Metadata storage
└── <collection_id>/
    ├── data_level0.bin          # Vector data
    ├── header.bin               # Index headers
    ├── length.bin               # Document lengths
    └── link_lists.bin           # HNSW graph
```

**Embedding Model:**
- **Model:** all-MiniLM-L6-v2
- **Dimensions:** 384
- **Source:** HuggingFace sentence-transformers
- **Speed:** Fast inference (~50ms per query)

**Search Algorithm:**
- HNSW (Hierarchical Navigable Small World)
- Cosine similarity metric
- Returns top-k documents (k=3 default)

---

### 4. LLM Service (Groq)

**Configuration:**
- **Model:** llama-3.3-70b-versatile
- **Temperature:** 0.1 (deterministic answers)
- **Max Tokens:** 1024
- **API:** Groq Cloud API

**Prompt Template:**
```
Use the following context to answer the question concisely and 
professionally as O.T.T.O (Smart Society Assistant).

Context:
{retrieved_documents}

Question: {user_query}

Answer:
```

**Why Groq?**
- Extremely fast inference (LPU architecture)
- Free tier available
- Superior speed/cost ratio
- Simple API integration

---

## 🗄️ Data Flow

### Document Ingestion (ingest.ipynb)

```
1. Source Documents
   ├── Data/md/Administrative & Legal/*.md
   ├── Data/md/Community & Lifestyle/*.md
   ├── Data/md/Digital Services/*.md
   └── ... (organized by category)
   
2. Loading & Chunking
   ↓
   • DirectoryLoader reads all .md files
   • RecursiveTextSplitter creates chunks
   • Chunk size: ~500 tokens
   • Overlap: ~50 tokens
   
3. Embedding Generation
   ↓
   • HuggingFace model processes each chunk
   • Generates 384-dimensional vectors
   
4. Vector Storage
   ↓
   • ChromaDB stores vectors + metadata
   • Builds HNSW index for fast search
   • Persists to Data/vectorstore/
```

### Query Processing (Runtime)

```
User Query → Embedding → Similarity Search → Top-K Docs → Context
                                                              ↓
User Query ← Markdown ← LLM Response ← Prompt Template ← Context
```

---

## 🔐 Security Considerations

### Current Implementation
⚠️ **API Key Hardcoded**: Groq API key is in source code
⚠️ **CORS Open**: Allows all origins (`allow_origins=["*"]`)
⚠️ **No Authentication**: Public endpoint, no rate limiting

### Recommended Improvements
✅ Use environment variables for API keys
✅ Restrict CORS to specific domains
✅ Implement API authentication (JWT/OAuth)
✅ Add rate limiting middleware
✅ Input validation and sanitization
✅ HTTPS in production

---

## ⚡ Performance Characteristics

### Latency Breakdown (Typical Query)

| Stage | Time | Notes |
|-------|------|-------|
| Frontend → Backend | ~10ms | Local network |
| Embedding Generation | ~50ms | CPU-based |
| Vector Search | ~20ms | HNSW fast |
| LLM Inference (Groq) | ~500-1000ms | Network + GPU |
| **Total** | **~600-1100ms** | Sub-2-second response |

### Bottlenecks
1. **LLM Inference** - Largest component (60-70% of time)
2. **Network Latency** - Groq API is cloud-based
3. **Embedding** - Can be optimized with GPU

### Optimizations
- ✅ HNSW index for fast search
- ✅ Low temperature for faster inference
- ✅ Async FastAPI for concurrency
- ⏳ Potential: Response streaming
- ⏳ Potential: Caching frequent queries

---

## 🔧 Technology Choices & Rationale

### Why ChromaDB?
- ✅ Embedded database (no server setup)
- ✅ Python-native integration
- ✅ Excellent documentation
- ✅ Active development
- ✅ Free and open-source

**Alternatives:** Pinecone (cloud), Weaviate (self-hosted), FAISS (Meta)

### Why FastAPI?
- ✅ Modern async framework
- ✅ Automatic OpenAPI docs
- ✅ Type hints and validation
- ✅ High performance
- ✅ Easy CORS handling

**Alternatives:** Flask (simpler), Django (heavier), Starlette (lower-level)

### Why Groq/Llama 3.3?
- ✅ State-of-the-art LLM (70B params)
- ✅ Lightning-fast inference
- ✅ Free tier available
- ✅ Simple API
- ✅ No fine-tuning needed

**Alternatives:** OpenAI GPT-4 (expensive), Anthropic Claude, Local LLMs (Ollama)

---

## 📊 Scalability Considerations

### Current Capacity
- **Documents:** ~40 markdown files
- **Vector DB Size:** ~few MB
- **Concurrent Users:** Limited by single FastAPI instance
- **Deployment:** Local development

### Scaling Path

**Phase 1: Single Server**
- Deploy on cloud VM (AWS EC2, DigitalOcean)
- Use Nginx reverse proxy
- PM2/systemd for process management

**Phase 2: Horizontal Scaling**
- Load balancer (Nginx/HAProxy)
- Multiple FastAPI instances
- Shared vector database (cloud ChromaDB or Pinecone)

**Phase 3: Microservices**
- Separate embedding service
- LLM gateway (rate limiting, caching)
- CDN for frontend
- Redis for caching

---

## 🧪 Testing Strategy

**Unit Tests:**
- RAGEngine methods
- API endpoints
- Utility functions

**Integration Tests:**
- Full RAG pipeline
- Database connectivity
- LLM API calls

**End-to-End Tests:**
- UI interactions
- Complete user flows
- Error scenarios

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Groq API Reference](https://console.groq.com/docs)
- [HuggingFace Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

---

**Next:** [Setup Guide](SETUP.md) | [API Reference](API_REFERENCE.md) | [Back to README](../README.md)
