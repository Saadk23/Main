import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Langfuse v4
from langfuse import get_client
from langfuse import propagate_attributes   # ← Add this import

load_dotenv()

langfuse = get_client()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
MODEL_NAME = "all-MiniLM-L6-v2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "Data", "vectorstore")


class RAGEngine:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1024
        )
        if os.path.exists(VECTOR_DB_PATH):
            self.vector_db = Chroma(
                persist_directory=VECTOR_DB_PATH,
                embedding_function=self.embeddings
            )
        else:
            self.vector_db = None
            print(f"⚠️ Vector DB not found at: {VECTOR_DB_PATH}")


engine = RAGEngine()

class ChatRequest(BaseModel):
    prompt: str
    session_id: str | None = None

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

@app.post("/ask")
async def ask_bot(request: ChatRequest):
    try:
        with langfuse.start_as_current_observation(
            as_type="span",
            name="chat-query",
            input={"prompt": request.prompt}
        ) as observation:

            with propagate_attributes(
                user_id="hanzala_user_1", 
                session_id=getattr(request, 'session_id', None)
            ):

                if engine.vector_db is None:
                    response_text = "Vector database not found. Please check your Data/vectorstore folder."
                else:
                    # Retrieval
                    retrieved_docs = engine.vector_db.similarity_search(request.prompt, k=5)  # increased to 5

                    if not retrieved_docs:
                        response_text = "I couldn't find any relevant information in my knowledge base."
                    else:
                        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

                        # Stronger, clearer RAG prompt (very important for Llama 3.3)
                        rag_prompt = f"""You are a helpful and accurate assistant.

Use ONLY the following context to answer the user's question.
If the answer is not present in the context, reply with: "I don't have that information in my knowledge base."

Context:
{context}

Question: {request.prompt}

Answer:"""

                        # Call LLM
                        response = engine.llm.invoke(rag_prompt)
                        response_text = response.content.strip()

                        # Optional: Add retrieval info for debugging in Langfuse
                        observation.update(
                            metadata={
                                "retrieved_chunks": len(retrieved_docs),
                                "context_length": len(context)
                            }
                        )

            # Update output in Langfuse
            observation.update(output=response_text)

            return {"answer": response_text}

    except Exception as e:
        print(f"❌ Error in /ask: {e}")
        return {"error": f"Internal error: {str(e)}"}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)