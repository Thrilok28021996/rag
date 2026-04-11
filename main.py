from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.prompts import ChatPromptTemplate

from langchain_ollama import ChatOllama

from utils import data_ingestion


file_path = "/Users/thrilok/Documents/princeton_bitcoin_book.pdf"


class RAG:
    def __init__(self, file_path):

        self.file_path = file_path
        vectorstore = data_ingestion(self.file_path)
        ## initialize the model
        llm = ChatOllama(
            model="llama3.2",  # or mistral / phi3 / gemma
            temperature=0,
        )
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 10}
        )  # top-4 relevant chunks

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

        print("Answer:")
        print(response["answer"])

        print("*" * 20)

        for doc in response["context"]:
            print(doc.page_content[:201])
        print("----")


RAG(file_path)
