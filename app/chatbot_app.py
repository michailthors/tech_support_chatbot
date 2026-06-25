import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/ask"

def chat(user_message, history):
    """
    Sends the user message to the FastAPI backend and returns the answer.
    """
    try:
        response = requests.post(API_URL, json={"question": user_message})
        answer = response.json()["answer"]
    except Exception as e:
        answer = f"Error connecting to API: {str(e)}"
    
    return answer

demo = gr.ChatInterface(
    fn=chat,
    title="🤖 Tech Support Chatbot",
    description="Ask me anything about your tech problems! I'm here to help.",
    examples=[
        "Why is my phone not turning on?",
        "My WiFi keeps disconnecting, what should I do?",
        "My laptop is running very slow, how can I fix it?",
        "I can't log into my account, what should I do?"
    ],
    
)

demo.launch(server_name="0.0.0.0", server_port=7860)