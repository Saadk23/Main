# Data Directory

This directory contains the knowledge base and vector database for the O.T.T.O Smart Society Assistant ChatBot.

---

## 📁 Directory Structure

```
Data/
├── md/                     # Source documents (Markdown files)
│   └── Smart Scociety/     # Main category folder
│       ├── Administrative & Legal/
│       ├── Archive & Future Developments/
│       ├── Community & Lifestyle/
│       ├── Digital Services & Smart App/
│       ├── Financials & Accounts/
│       ├── Infrastructure & Security/
│       └── Operations & Utilities/
│
└── vectorstore/            # ChromaDB vector database
   ├── chroma.sqlite3      # Metadata database
    └── <collection-ids>/   # Embedding vectors
        ├── data_level0.bin
        ├── header.bin
        ├── length.bin
        └── link_lists.bin
```

---

## 📄 Markdown Files (`md/`)

### Purpose
Contains 33+ markdown files with information about Smart Society rules, facilities, services, and policies.

### Content Categories

#### 1. **Administrative & Legal** (4 files)
- Dispute Resolution
- Property Transfer & Ownership
- Relocation Policy
- Society Elections

#### 2. **Archive & Future Developments** (2 files)
- Newsletter 2026
- Upcoming Projects

#### 3. **Community & Lifestyle** (13 files)
- Co-working Space
- Community Kitchen
- Guest House
- Shuttle Service
- Prayer Rooms
- Outdoor Cinema
- Pet Grooming
- Senior Citizen Lounge
- Smart Parcel Lockers
- Utility Services
- Waste Management/Recycling
- Water Management

#### 4. **Digital Services & Smart App** (2 files)
- App Troubleshooting
- Visitor QR System

#### 5. **Financials & Accounts** (2 files)
- Property Tax Guide
- Surcharge & Arrears Policy

#### 6. **Infrastructure & Security** (4 files)
- Commercial Area Rules
- Construction Rules
- General Security
- RFID Systems

#### 7. **Operations & Utilities** (6 files)
- Emergency Procedures
- Environmental & Plantation
- Facilities & Amenities
- Library
- Pet Ownership Bylaws

---

## 🗄️ Vector Database (`vectorstore/`)

### Purpose
ChromaDB vector database storing document embeddings for semantic search.

### Structure

**chroma.sqlite3**
- Metadata storage
- Document IDs and collections
- Index structure

**Collection Folders** (UUID names)
- **data_level0.bin**: Vector embeddings (384 dimensions)
- **header.bin**: Index headers
- **length.bin**: Document lengths
- **link_lists.bin**: HNSW graph for fast search

### Statistics
- **Total Documents**: 33 markdown files
- **Embedding Model**: all-MiniLM-L6-v2
- **Vector Dimensions**: 384
- **Search Algorithm**: HNSW (Hierarchical Navigable Small World)

---

## ➕ Adding New Documents

### Step 1: Create Markdown File

```bash
# Navigate to appropriate category
cd Data/md/Smart Scociety/Community & Lifestyle/

# Create new file
echo "# New Facility\n\nDescription..." > New_Facility.md
```

### Step 2: Follow Format Guidelines

```markdown
# Title with Emoji

Brief introduction paragraph.

## 1. Section Heading

- Bullet points
- Key information

## 2. Another Section

Tables for structured data:

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

### Step 3: Update Vector Database

```bash
# Open ingest notebook
jupyter notebook notebook/ingest.ipynb

# Run all cells
# Or use brain.ipynb for custom processing
```

### Step 4: Restart Backend

```bash
# Restart FastAPI server to load new data
python main.py
```

---

## 📝 File Naming Conventions

### Best Practices
- Use descriptive names
- Separate words with underscores
- Use title case
- Add `.md` extension

### Examples
✅ **Good:**
- `Swimming_Pool_Rules.md`
- `Gym_Timings.md`
- `Pet_Ownership_Bylaws.md`

❌ **Avoid:**
- `file1.md` (not descriptive)
- `swimming-pool-rules.md` (use underscores)
- `POOL_RULES.md` (avoid all caps)

---

## 🎨 Markdown Formatting

### Use Emojis for Visual Appeal
```markdown
🏊 Swimming Pool Rules
📚 Library Guidelines
🚗 Parking Regulations
```

### Structure Content Clearly
```markdown
# Main Title

Brief introduction

## 1. First Topic

Detailed explanation

## 2. Second Topic

More details
```

### Use Tables for Data
```markdown
| Facility | Timing | Charges |
|----------|--------|---------|
| Pool     | 7-9 PM | Rs. 500 |
```

---

## 🔍 Search & Retrieval

### How Vector Search Works

1. **User Query**: "What are the pool timings?"
2. **Embedding**: Convert query to 384-dim vector
3. **Search**: Find top-k similar documents in vectorstore
4. **Context**: Extract relevant text chunks
5. **LLM**: Generate answer using context

### Similarity Scoring
- Uses cosine similarity
- Range: 0.0 to 1.0
- Higher score = more relevant

---

## 🧹 Maintenance

### Clean Vector Database

```bash
# Backup current database
cp -r Data/vectorstore Data/vectorstore_backup

# Delete database
rm -rf Data/vectorstore

# Recreate from markdown files
jupyter notebook notebook/ingest.ipynb
```

### verify Database

Check database stats in Python:

```python
import chromadb

client = chromadb.PersistentClient(path="Data/vectorstore")
collection = client.get_collection("pdf_documents")

print(f"Total documents: {collection.count()}")
```

---

## 📊 Database Statistics

```bash
# Check database size
# Windows
dir Data\vectorstore /s

# macOS/Linux
du -sh Data/vectorstore
```

**Expected Size**: 5-50 MB (depends on number of documents)

---

## 🚫 What NOT to Store

❌ **Don't include:**
- Personal information (CNIC, phone numbers)
- Sensitive financial data
- Private correspondence
- Binary files (images, PDFs) - only markdown
- Temporary/draft documents

✅ **Do include:**
- Society rules and policies
- Facility information
- Contact information (official only)
- Procedures and guidelines
- FAQ content

---

## 🔐 Security Notes

- The vector database is stored locally
- No sensitive data should be in markdown files
- API keys are NOT stored in this directory
- Backup important documents regularly

---

## 📚 Learn More

- [Notebook Guide](../notebook/README.md) - How to process documents
- [Architecture](../docs/ARCHITECTURE.md) - RAG system design
- [Backend Documentation](../docs/MAIN_PY.md) - How data is used

---

**Summary:** This directory powers the knowledge base of O.T.T.O chatbot. Markdown files contain society information, and the vector database enables semantic search for intelligent responses.
