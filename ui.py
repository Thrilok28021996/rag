import streamlit as st
from main import get_answer
from utils import data_ingestion

st.title("RAG")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


upload_file = st.file_uploader("Upload an File", type=["pdf"])
if upload_file and upload_file.name != st.session_state.get("file_name"):
    st.session_state.vectorstore = data_ingestion(upload_file)
    st.session_state.file_name = upload_file.name
    st.session_state.messages = []  # reset chat on new doc

# Replay history on every rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New question
if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_answer(st.session_state.vectorstore, prompt)
    st.session_state.messages.append(
        {"role": "assistant", "content": response["answer"]}
    )
    st.rerun()
