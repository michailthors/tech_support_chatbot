import chromadb
from sentence_transformers import SentenceTransformer
from document_loader import load_twitter_data

def create_vector_store(filepath: str, max_pairs: int = 5000):
    """
    Creates a ChromaDB vector store from twitter data.
    """
    # Loading Data
    pairs = load_twitter_data(filepath, max_pairs)

    # Loading sentence transformer model
    print("⏳ Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Connect with ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")
    
    # Delete of old collection.
    try:
        client.delete_collection("twitter_support")
    except:
        pass

    collection = client.create_collection("twitter_support")

    # Προσθήκη δεδομένων σε batches
    print("⏳ Creation of embeddings and saved into ChromaDB...")
    
    batch_size = 500
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i+batch_size]
        
        documents = [p['question'] for p in batch]
        metadatas = [{'answer': p['answer'], 'company': p['company']} for p in batch]
        ids = [f"doc_{i+j}" for j in range(len(batch))]
        embeddings = model.encode(documents).tolist()

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        
        print(f"✅ Batch {i//batch_size + 1} saved ({min(i+batch_size, len(pairs))}/{len(pairs)})")

    print(f"\n✅ Vector store ready! {collection.count()} documents in ChromaDB")
    return collection


if __name__ == "__main__":
    create_vector_store('data/twcs.csv')