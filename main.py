from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = "/Users/thrilok/Documents/princeton_bitcoin_book.pdf"
loader = PyMuPDFLoader(file_path)
documents = loader.load()
embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest",
)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
texts = text_splitter.split_documents(documents)
# print("texts", texts)

# Create a vector store with a sample text
vectorstore = InMemoryVectorStore.from_documents(
    texts,
    embedding=embeddings,
)

# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()

retrieved_documents = retriever.invoke("What is bitcoin?")

for i, doc in enumerate(retrieved_documents):
    print(f"\n=== Result {i} ===")
    print(doc.page_content.replace("\xa0", " ")[:500])
