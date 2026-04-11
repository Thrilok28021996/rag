
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader


def data_ingestion(file_path):
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    embeddings= OllamaEmbeddings(model="nomic-embed-text:latest")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=150,add_start_index=True)
    texts = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(texts,embeddings)

    return vectorstore
