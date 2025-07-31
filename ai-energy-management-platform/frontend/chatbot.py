import streamlit as st
import openai  # Optional: Use only if you have API key
import os
openai.api_key = "your-key"
openai.Model.list()

st.set_page_config(page_title="Energy Assistant Chatbot", layout="wide")
st.title("🤖 AI Energy Assistant")

st.markdown("Ask me anything about energy usage, optimization, or smart home energy tips!")

# Optional: Set your API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")  # or set directly if testing

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
user_input = st.chat_input("Type your energy question here...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Simulate or call OpenAI (if available)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to any available model
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
    except:
        reply = "⚠️ I'm running in offline mode. Here's a static answer:\n\n" \
                "Try reducing energy usage during peak hours (6–10 PM) and using energy-efficient appliances."

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
