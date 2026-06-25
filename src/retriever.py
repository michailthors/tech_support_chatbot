import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Loading models
model = SentenceTransformer('all-MiniLM-L6-v2')
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Connect with ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_collection("twitter_support")


def retrieve_and_answer(user_question: str, n_results: int = 3) -> str:
    """
    Finds similar pairs from ChromaDB and answers through Groq.
    """
    # Step 1: Question converter into vector
    question_embedding = model.encode(user_question).tolist()

    # Step 2: Search in ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    # Step 3: Creating context from results.
    context = ""
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        context += f"Example {i+1}:\n"
        context += f"Customer Question: {doc}\n"
        context += f"Support Answer: {metadata['answer']}\n\n"

    # Βήμα 4: Αποστολή στο Groq LLM
    prompt = f"""You are a helpful technical support assistant.
Based on the following examples from real customer support conversations, answer the user's question.


Examples:
{context}

User Question: {user_question}

Give a comprehensive and helpful answer in English."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Test
    question = "Why my phone is not turning on?"
    print(f"Question: {question}")
    print(f"\nAnswer: {retrieve_and_answer(question)}")