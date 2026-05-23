# API Reference

Complete API documentation for the O.T.T.O ChatBot backend.

---

## 🌐 Base URL

**Development:** `http://127.0.0.1:8000`  
**Production:** `https://your-domain.com` (configure as needed)

---

## 📡 Endpoints

### POST /ask

Send a question to the O.T.T.O chatbot and receive an AI-generated response.

---

#### Request

**Method:** `POST`  
**Endpoint:** `/ask`  
**Content-Type:** `application/json`

**Request Body:**
```json
{
  "prompt": "string (required)"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | ✅ Yes | User's question or message |

**Example Request:**
```json
{
  "prompt": "What are the swimming pool timings?"
}
```

---

#### Response

**Content-Type:** `application/json`

**Success Response (200 OK):**
```json
{
  "answer": "string",
  "status": "success"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | Bot's response (may include Markdown) |
| `status` | string | Either "success" or "error" |

---

#### Example Responses

**1. Greeting Response:**

Request:
```json
{
  "prompt": "Hello"
}
```

Response:
```json
{
  "answer": "Hello! I am O.T.T.O. How can I assist you with society matters today?",
  "status": "success"
}
```

---

**2. Knowledge Query Response:**

Request:
```json
{
  "prompt": "What facilities are available in the society?"
}
```

Response:
```json
{
  "answer": "The Smart Society offers various facilities including:\n\n**Sports & Recreation:**\n- Swimming pool (6 AM - 10 PM)\n- Gymnasium (24/7 access)\n- Tennis courts\n- Outdoor cinema\n\n**Community Services:**\n- Co-working space\n- Library & reading lounge\n- Community kitchen\n- Guest house\n\nFor more details about specific facilities, please let me know!",
  "status": "success"
}
```

---

**3. Error Response (Database Missing):**

Response:
```json
{
  "answer": "Error: Database not found.",
  "status": "success"
}
```

---

**4. Error Response (Server Error):**

Response:
```json
{
  "answer": "System Error: API key invalid",
  "status": "error"
}
```

---

## 🔧 HTTP Examples

### Using cURL

**Basic Request:**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

**With Pretty Print:**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the gym timings?"}' \
  | python -m json.tool
```

---

### Using PowerShell (Windows)

```powershell
$body = @{
    prompt = "What are the pool timings?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

---

### Using Python (requests)

```python
import requests

url = "http://127.0.0.1:8000/ask"
payload = {"prompt": "What are the facilities?"}

response = requests.post(url, json=payload)
data = response.json()

print(data["answer"])
```

---

### Using JavaScript (Fetch API)

```javascript
async function askOTTO(question) {
  const response = await fetch('http://127.0.0.1:8000/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ prompt: question })
  });
  
  const data = await response.json();
  return data.answer;
}

// Usage
const answer = await askOTTO("What are the swimming pool timings?");
console.log(answer);
```

---

## 📊 Response Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200 OK** | Success | Request processed successfully |
| **422 Unprocessable Entity** | Validation Error | Invalid request format (missing `prompt`) |
| **500 Internal Server Error** | Server Error | Backend error (caught by try/catch) |

---

## ⚡ Rate Limiting

**Current:** No rate limiting (development)

**Production Recommendations:**
- Implement rate limiting (e.g., 60 requests/minute per IP)
- Use middleware like `slowapi`

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/ask")
@limiter.limit("60/minute")
async def ask_bot(request: ChatRequest):
    ...
```

---

## 🔐 Authentication

**Current:** None (public endpoint)

**Production Recommendations:**

### Option 1: API Key Authentication

```python
from fastapi import Header, HTTPException

@app.post("/ask")
async def ask_bot(
    request: ChatRequest,
    x_api_key: str = Header(...)
):
    if x_api_key != "your_secret_key":
        raise HTTPException(status_code=401, detail="Invalid API key")
    ...
```

**Usage:**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_secret_key" \
  -d '{"prompt": "Hello"}'
```

---

### Option 2: JWT Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "valid_jwt_token":
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/ask")
async def ask_bot(request: ChatRequest, token = Depends(verify_token)):
    ...
```

---

## 🧪 Interactive API Documentation

FastAPI provides automatic interactive documentation:

### Swagger UI (Recommended)

**URL:** `http://127.0.0.1:8000/docs`

**Features:**
- Try out API directly in browser
- See request/response schemas
- Download OpenAPI spec

### ReDoc (Alternative)

**URL:** `http://127.0.0.1:8000/redoc`

**Features:**
- Clean, readable documentation
- Three-panel layout
- Downloadable OpenAPI spec

---

## 📝 OpenAPI Schema

**URL:** `http://127.0.0.1:8000/openapi.json`

Export the schema for code generation, testing, or documentation tools.

---

## 🔄 CORS Configuration

**Current Settings:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # All origins
    allow_methods=["*"],          # All HTTP methods
    allow_headers=["*"],          # All headers
)
```

**Production Recommendation:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

## 🐛 Error Handling

### Validation Errors (422)

**Example:** Missing `prompt` field

Request:
```json
{}
```

Response:
```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### Server Errors (Handled)

Caught by try/catch block in endpoint:

```json
{
  "answer": "System Error: <error message>",
  "status": "error"
}
```

Common errors:
- `API key invalid` - Groq API key issue
- `Connection refused` - Network issue
- `Timeout` - Slow LLM response

---

## 📈 Performance

### Typical Response Times

| Query Type | Time | Notes |
|------------|------|-------|
| Greeting (cached) | ~10ms | No LLM call |
| Simple query | ~600-1000ms | Embedding + search + LLM |
| Complex query | ~1000-1500ms | Longer generation |

**Bottleneck:** Groq LLM inference (~60-70% of total time)

---

### Optimization Tips

1. **Reduce `k` in similarity search:**
   ```python
   docs = self.vector_db.similarity_search(query, k=2)  # Instead of k=3
   ```

2. **Lower `max_tokens`:**
   ```python
   self.llm = ChatGroq(..., max_tokens=512)  # Faster responses
   ```

3. **Enable caching** (for repeated queries):
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_get_answer(query: str):
       return engine.get_answer(query)
   ```

---

## 🧪 Testing the API

### Unit Tests (pytest)

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_greeting():
    response = client.post("/ask", json={"prompt": "Hello"})
    assert response.status_code == 200
    assert "O.T.T.O" in response.json()["answer"]

def test_knowledge_query():
    response = client.post("/ask", json={"prompt": "What are the facilities?"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_empty_prompt():
    response = client.post("/ask", json={})
    assert response.status_code == 422
```

Run tests:
```bash
pytest test_main.py
```

---

### Load Testing

Using Apache Bench:
```bash
ab -n 100 -c 10 -p request.json -T application/json http://127.0.0.1:8000/ask
```

Where `request.json`:
```json
{"prompt": "Hello"}
```

---

## 📚 Additional Endpoints (Future)

### GET /health (Recommended)

Health check endpoint for monitoring:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected" if engine.vector_db else "disconnected",
        "llm": "ready"
    }
```

---

### GET /stats (Future Enhancement)

Usage statistics:

```python
@app.get("/stats")
async def get_stats():
    return {
        "total_queries": 1234,
        "average_response_time": "850ms",
        "uptime": "5 days"
    }
```

---

## 🔗 Integration Examples

### React Integration

```jsx
import { useState } from 'react';

function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  
  const sendMessage = async () => {
    const response = await fetch('http://127.0.0.1:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: input })
    });
    
    const data = await response.json();
    setMessages([...messages, { user: input, bot: data.answer }]);
    setInput('');
  };
  
  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>
          <p>User: {msg.user}</p>
          <p>Bot: {msg.bot}</p>
        </div>
      ))}
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
```

---

### Mobile App (React Native)

```javascript
const askBot = async (question) => {
  try {
    const response = await fetch('http://your-server.com/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: question })
    });
    
    const data = await response.json();
    return data.answer;
  } catch (error) {
    console.error('Error:', error);
    return 'Connection error';
  }
};
```

---

## 📖 Best Practices

1. ✅ **Always handle errors** - Network can fail
2. ✅ **Validate responses** - Check `status` field
3. ✅ **Show loading state** - Responses take ~1 second
4. ✅ **Parse Markdown** - Bot responses may include formatting
5. ✅ **Implement retry logic** - For transient failures
6. ✅ **Use HTTPS in production** - Secure communication
7. ✅ **Cache responses** - For repeated queries

---

## 📞 Support

For API issues:
- Check server logs
- Verify backend is running
- Test with Swagger UI (`/docs`)
- Review [Backend Documentation](MAIN_PY.md)

---

**Next:** [Developer Guide](DEVELOPER_GUIDE.md) | [Architecture](ARCHITECTURE.md) | [Back to README](../README.md)
