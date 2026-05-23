# Setup & Installation Guide

Complete guide to setting up the O.T.T.O Smart Society Assistant ChatBot on your local machine.

---

## 📋 Prerequisites

### Required Software

| Software | Version | Purpose | Download Link |
|----------|---------|---------|---------------|
| **Python** | 3.11+ | Backend runtime | [python.org](https://www.python.org/downloads/) |
| **Git** | Latest | Version control | [git-scm.com](https://git-scm.com/) |
| **Text Editor** | Any | Code editing | [VS Code](https://code.visualstudio.com/) (recommended) |

### Optional Tools

- **UV Package Manager** - Fast Python package installer (recommended)
- **Jupyter** - For running development notebooks
- **Postman** - For API testing

### Account Requirements

- **Groq API Account** - Free tier available at [console.groq.com](https://console.groq.com)

---

## 🚀 Installation Steps

### 1. Clone the Repository

```bash
# Clone the project
git clone <repository-url>
cd ChatBot

# Verify files
ls
```

**Expected output:**
```
Data/
notebook/
main.py
index.html
README.md
requirements.txt
pyproject.toml
```

---

### 2. Set Up Python Environment

#### Option A: Using UV (Recommended)

```bash
# Install UV (if not already installed)
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync
```

#### Option B: Using pip + venv

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Get Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy the generated key (starts with `gsk_...`)

⚠️ **Important:** Save this key securely - you won't be able to see it again!

---

### 4. Configure API Key

Open `main.py` and update line 23:

```python
# BEFORE (line 23)
GROQ_API_KEY = "your_actual_groq_api_key_here"

# AFTER
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

**Better Practice:** Use environment variables

```python
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "default_key")
```

Then set the environment variable:
```bash
# Windows
set GROQ_API_KEY=your_key_here

# macOS/Linux
export GROQ_API_KEY=your_key_here
```

---

### 5. Verify Vector Database

Check that the vector database exists:

```bash
# Windows
dir Data\vectorstore

# macOS/Linux
ls Data/vectorstore
```

**Expected files:**
- `chroma.sqlite3`
- Folders with UUIDs containing `.bin` files

**If missing:** Run the `notebook/ingest.ipynb` notebook to generate the database (see [Notebook Guide](../notebook/README.md)).

---

### 6. Run the Backend

```bash
# Activate virtual environment (if not already active)
# Windows
.venv\Scripts\activate

# Run the FastAPI server
python main.py
```

**Expected output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

✅ **Backend is running!**

---

### 7. Open the Frontend

#### Option A: Direct File Open (Simple)

```bash
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

#### Option B: Run Local Server (Recommended)

```bash
# Open new terminal, navigate to project directory
cd ChatBot

# Start simple HTTP server
python -m http.server 3000
```

Then open browser: `http://localhost:3000/index.html`

---

### 8. Test the Chatbot

1. Click the **purple chat icon** in bottom-right corner
2. Type a greeting: `Hello`
3. Expected response: `Hello! I am O.T.T.O. How can I assist you with society matters today?`
4. Ask a question: `What are the facilities available?`
5. Should receive a detailed answer based on the knowledge base

---

## 🧪 Verify Installation

### Test Backend Directly

```bash
# Using curl (macOS/Linux)
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'

# Using PowerShell (Windows)
Invoke-RestMethod -Uri http://127.0.0.1:8000/ask -Method POST -Body '{"prompt":"Hello"}' -ContentType "application/json"
```

**Expected response:**
```json
{
  "answer": "Hello! I am O.T.T.O. How can I assist you with society matters today?",
  "status": "success"
}
```

### Check FastAPI Docs

Visit: `http://127.0.0.1:8000/docs`

You'll see the interactive API documentation (Swagger UI).

---

## 🔧 Troubleshooting

### Issue: `Module not found` errors

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
# or
uv sync
```

---

### Issue: `Database not found` error

**Cause:** Vector database doesn't exist

**Solution:**
1. Check if `Data/vectorstore/` exists
2. Run `notebook/ingest.ipynb` to create the database
3. Restart `main.py`

---

### Issue: `CORS error` in browser console

**Cause:** Backend not running or wrong URL

**Solution:**
1. Ensure `main.py` is running
2. Check backend URL in `index.html` (line 136):
   ```javascript
   const response = await fetch('http://127.0.0.1:8000/ask', ...)
   ```
3. Verify CORS is enabled in `main.py` (lines 12-17)

---

### Issue: API key errors from Groq

**Cause:** Invalid or missing API key

**Solution:**
1. Verify your API key at [console.groq.com](https://console.groq.com)
2. Check for typos in `main.py`
3. Ensure no extra spaces or quotes
4. Try generating a new API key

---

### Issue: Slow responses

**Possible causes:**
- Slow internet connection
- Groq API rate limits
- Large document retrieval

**Solutions:**
- Reduce `k` parameter in similarity search (line 52)
- Decrease `max_tokens` in LLM config (line 35)
- Check Groq API status

---

### Issue: Port 8000 already in use

**Solution:**
```python
# Edit main.py, line 95
uvicorn.run(app, host="127.0.0.1", port=8001)  # Change port
```

Don't forget to update `index.html` line 136 to match!

---

## 🔐 Security Best Practices

### For Development

1. **Never commit API keys** to Git
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   GROQ_API_KEY = os.getenv("GROQ_API_KEY")
   ```

3. **Install python-dotenv**
   ```bash
   pip install python-dotenv
   ```

4. **Create `.env` file**
   ```
   GROQ_API_KEY=your_actual_key_here
   ```

---

### For Production

1. ✅ Use HTTPS
2. ✅ Set specific CORS origins
3. ✅ Add authentication
4. ✅ Implement rate limiting
5. ✅ Use secrets management (AWS Secrets Manager, Azure Key Vault)

---

## 📦 Optional: Jupyter Notebooks Setup

If you want to run the development notebooks:

```bash
# Install Jupyter
pip install jupyter notebook

# Start Jupyter
jupyter notebook

# Navigate to notebook/ folder
# Open brain.ipynb or ingest.ipynb
```

---

## 🐳 Optional: Docker Setup

Create `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t otto-chatbot .
docker run -p 8000:8000 otto-chatbot
```

---

## 🚀 Deployment Options

### Cloud Platforms

| Platform | Difficulty | Cost | Guide |
|----------|-----------|------|-------|
| **Heroku** | Easy | Free tier | [Heroku Python](https://devcenter.heroku.com/articles/getting-started-with-python) |
| **Railway** | Easy | Free tier | [Railway Docs](https://docs.railway.app/) |
| **AWS EC2** | Medium | Pay-as-you-go | AWS tutorials |
| **DigitalOcean** | Medium | $5/month | DigitalOcean docs |
| **Vercel** | Easy (frontend only) | Free | For `index.html` |

### Deployment Checklist

- [ ] Set API key as environment variable
- [ ] Configure CORS for production domain
- [ ] Use HTTPS
- [ ] Set up monitoring (logs, errors)
- [ ] Configure auto-restart (PM2, systemd)
- [ ] Set up backups for vector database
- [ ] Add rate limiting
- [ ] Implement authentication

---

## 📚 Next Steps

After successful installation:

1. **Read Architecture** - [docs/ARCHITECTURE.md](ARCHITECTURE.md)
2. **Explore Code** - [docs/MAIN_PY.md](MAIN_PY.md)
3. **Customize UI** - [docs/INDEX_HTML.md](INDEX_HTML.md)
4. **Add Data** - [notebook/README.md](../notebook/README.md)
5. **API Integration** - [docs/API_REFERENCE.md](API_REFERENCE.md)

---

## 💬 Need Help?

- Check [Troubleshooting](#-troubleshooting) section above
- Review [Developer Guide](DEVELOPER_GUIDE.md)
- Check GitHub issues
- Contact the development team

---

**Next:** [Architecture Guide](ARCHITECTURE.md) | [API Reference](API_REFERENCE.md) | [Back to README](../README.md)
