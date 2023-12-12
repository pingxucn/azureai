import streamlit as st
from openai import OpenAI
import os
from Sql_python_document_agents import agent_executor

st.title("Data Analysis")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
with st.sidebar:
    with open("DatabaseDiagrams.png", "rb") as f:
        pdf_bytes = f.read()
        st.download_button(
            label="Database Diagrams",
            data=pdf_bytes,
            file_name="DatabaseDiagrams.png",
            mime="application/png",
        )

with st.sidebar:
    with open("DataAnalysis.docx", "rb") as f:
        pdf_bytes = f.read()
        st.download_button(
            label="Download Report",
            data=pdf_bytes,
            file_name="DataAnalysis.docx",
            mime="application/docx",
        )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = agent_executor(prompt)
        print(f"full_response : {full_response}")
        # message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})        