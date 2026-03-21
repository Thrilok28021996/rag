from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = "/Users/thrilok/Documents/princeton_bitcoin_book.pdf"
loader = PyMuPDFLoader(file_path)
documents = loader.load()
embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest",
)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800, chunk_overlap=150, add_start_index=True
)
texts = text_splitter.split_documents(documents)
# print("texts", texts)


# Create a vector store with a sample text
# FAISS vector store
vectorstore = FAISS.from_documents(texts, embeddings)


## initialize the model
llm = ChatOllama(
    model="llama3.2",  # or mistral / phi3 / gemma
    temperature=0,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  # top-4 relevant chunks


## Define prompt
prompt = ChatPromptTemplate.from_template("""
You are a precise assistant. Answer ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{input}
""")

document_chain = create_stuff_documents_chain(llm, prompt)

rag_chain = create_retrieval_chain(retriever, document_chain)


response = rag_chain.invoke({"input": "What is Bitcoin mining?"})

print(response["answer"])

for doc in response["context"]:
    print(doc.page_content[:201])
    print("----")
