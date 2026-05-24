from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
import os


import tempfile


def data_ingestion(uploaded_file):
    # Save uploaded file to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    loader = PyMuPDFLoader(temp_path)
    documents = loader.load()

    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=150, add_start_index=True
    )

    texts = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(texts, embeddings)

    return vectorstore
