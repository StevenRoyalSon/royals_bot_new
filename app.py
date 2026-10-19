# Beginner HR chatbot using Streamlit and the OpenAI Responses API
import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent / ".env")

st.title("HR Chatbot")
st.caption("I can help with company policy, the job process, and the interview process.")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY is missing. Put it in the .env file next to app.py.")
    st.stop()

client = OpenAI(api_key=api_key)

HR_INSTRUCTIONS = """
You are a beginner-level HR assistant chatbot.

You may ONLY answer questions about:
1. Company policy
2. Job process (how to apply, hiring steps, onboarding)
3. Interview process

If the user asks about anything else, reply clearly:
"I am not responsible to explain that. I can only help with company policy, the job process, and the interview process. Please ask about one of those topics."

Keep answers short and easy to understand.
After you answer, invite the user to ask another question.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def get_response(history):
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=HR_INSTRUCTIONS,
        input=history,
    )
    return response.output_text

user_input = st.chat_input("Ask about company policy, job process, or interview process")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    reply = get_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
