from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
import subprocess
from database import get_db
from utils.vector_store import get_chroma_client
from src.api_schemas.chat import SearchQuery, ChatQuery


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])



# Initialize model once (optimization)
model = SentenceTransformer("all-MiniLM-L6-v2")


@router.post("/search")
def semantic_search(request: SearchQuery, db: Session = Depends(get_db)):
    """Search for laptops using semantic similarity"""
    try:
        client = get_chroma_client()
        collection = client.get_or_create_collection("laptops")
        
        # Convert query to embedding
        query_embedding = model.encode([request.query]).tolist()[0]
        
        # Search similar vectors
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        # Return top matches
        return {
            "query": request.query,
            "matches": results["metadatas"][0] if results["metadatas"] else [],
            "documents": results["documents"][0] if results["documents"] else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


def run_llm(prompt: str) -> str:
    """Run Ollama Mistral model with error handling"""
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            timeout=30  # Add timeout to prevent hanging
        )
        
        if result.returncode != 0:
            return f"Error running LLM: {result.stderr}"
        
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "LLM request timed out"
    except FileNotFoundError:
        return "Ollama not found. Please install Ollama first."
    except Exception as e:
        return f"Error: {str(e)}"


@router.post("/ask")
def chatbot(request: ChatQuery, db: Session = Depends(get_db)):
    """Ask questions about laptops using RAG (Retrieval Augmented Generation)"""
    try:
        client = get_chroma_client()
        collection = client.get_or_create_collection("laptops")
        
        # Get query embedding
        query_embedding = model.encode([request.query]).tolist()[0]
        
        # Search for relevant laptops
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        # Build context for LLM
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        
        if not documents:
            return {
                "response": "I couldn't find any relevant laptops. The vector store might be empty.",
                "matches": []
            }
        
        # Create prompt for LLM
        prompt = f"""You are a helpful laptop shopping assistant.

                    User asked: "{request.query}"

                    Here are the relevant laptops from our database:
                    {chr(10).join([f"- {doc}" for doc in documents])}

                    Provide a helpful, conversational response to the user's question based on these laptops. 
                    Be specific about the models and their features. Keep your response concise and friendly.

                    """
        
        # Get LLM response
        response = run_llm(prompt)
        
        return {
            "response": response,
            "matches": metadatas,
            "source_documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot failed: {str(e)}")
