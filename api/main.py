import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi import FastAPI
from pydantic import BaseModel
from retriever import retrieve_and_answer

app = FastAPI(
    title="Tech Support Chatbot API",
    description="A RAG-based chatbot that answers tech support questions using real customer support data.",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str

@app.get("/")
def root():
    return {"message": "Tech Support Chatbot API is running!"}

@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    """
    Receives a tech support question and returns an AI-generated answer
    based on real customer support conversations.
    """
    answer = retrieve_and_answer(request.question)
    return AnswerResponse(question=request.question, answer=answer)