from sentence_transformers import SentenceTransformer
import chromadb
from sqlalchemy.orm import Session
from src.models.Laptop_model import Laptop

# CRITICAL FIX: Use persistent client instead of ephemeral client
def get_chroma_client():
    """Get or create a persistent ChromaDB client"""
    return chromadb.PersistentClient(path="./chroma_db")

def build_vector_store(db: Session):
    """Build vector store from laptop database"""
    # Step 1: Load model for embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Step 2: Initialize Chroma client (FIXED: Use persistent client)
    client = get_chroma_client()
    
    # Delete existing collection to rebuild fresh
    try:
        client.delete_collection("laptops")
    except:
        pass
    
    collection = client.get_or_create_collection("laptops")
    
    # Step 3: Get all laptops
    laptops = db.query(Laptop).all()
    
    if not laptops:
        print("⚠️ No laptops found in database")
        return collection
    
    # Step 4: Convert to text for embedding
    texts = [f"{l.name} {l.brand} {l.specs} Price: ${l.price}" for l in laptops]
    ids = [str(l.id) for l in laptops]
    
    # Step 5: Generate embeddings
    embeddings = model.encode(texts).tolist()
    
    # Step 6: Store in ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"name": l.name, "price": float(l.price), "brand": l.brand} for l in laptops]
    )
    
    print(f"✅ Stored {len(laptops)} laptops as vectors")
    return collection