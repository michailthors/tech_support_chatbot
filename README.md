# 🤖 Tech Support Chatbot with RAG

A RAG-based Tech Support Chatbot that answers customer support questions using real Twitter support conversations. Built with Groq API (Llama 3.3 70B), ChromaDB, sentence-transformers, FastAPI, Gradio, and Docker.

## 📸 Screenshots
![](screenshots/tech0)
![](screenshots/tech1)
![](screenshots/tech2)
![](screenshots/tech3)
![](screenshots/tech4)
## 🏗️ Architecture

The chatbot uses a RAG (Retrieval-Augmented Generation) pipeline:

1. **Data Loading** - 5,000 real customer support Q&A pairs from the Twitter Customer Support dataset
2. **Embeddings** - Sentences are converted to vectors using `sentence-transformers` (all-MiniLM-L6-v2)
3. **Vector Store** - Vectors are stored in ChromaDB for fast similarity search
4. **Retrieval** - When a user asks a question, the most relevant Q&A pairs are retrieved
5. **Generation** - Groq API (Llama 3.3 70B) generates a comprehensive answer based on the retrieved context

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq API (Llama 3.3 70B) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB |
| Backend | FastAPI |
| Frontend | Gradio |
| Containerization | Docker |

## 📁 Project Structure
tech_support_chatbot/

├── notebooks/

│   └── 01_rag_pipeline.ipynb

├── src/

│   ├── document_loader.py    # loads and processes the dataset

│   ├── embeddings.py         # creates and stores vectors in ChromaDB

│   └── retriever.py          # RAG pipeline with Groq LLM

├── api/

│   └── main.py               # FastAPI REST API

├── app/

│   └── chatbot_app.py        # Gradio UI

├── data/                     # place twcs.csv here

├── chroma_db/                # auto-generated vector store

├── Dockerfile

├── docker-compose.yml

└── requirements.txt

## 🚀 Getting Started

### Prerequisites
- Docker Desktop
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Twitter Customer Support dataset (`twcs.csv`) from [Kaggle](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/michailthors/tech_support_chatbot.git
cd tech_support_chatbot
```

2. Create a `.env` file in the root directory:

3. Place `twcs.csv` inside the `data/` folder.

4. Build the vector store:
```bash
python src/embeddings.py
```

5. Run with Docker:
```bash
docker-compose up --build
```

6. Open your browser:
- **Gradio UI**: http://localhost:7860
- **FastAPI docs**: http://localhost:8000/docs

## 📊 Dataset

[Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter) — Over 3 million tweets and replies from the biggest brands on Twitter including Apple, Amazon, Uber, Spotify and more.

## 📝 License
MIT