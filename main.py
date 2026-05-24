from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.prompts import ChatPromptTemplate

from langchain_ollama import ChatOllama

from utils import data_ingestion
import streamlit as st

# folder_path = "docs"
from evaluate import faithfulness, answer_relevancy, context_relevancy


def get_answer(vectorstore,question):


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

    response = rag_chain.invoke({"input":question})
    return response



class RAG:
    def __init__(self, path, question):

        self.path = path
        self.question = question
        vectorstore = data_ingestion(self.path)

        print("*" * 20)
        # answer
        response = get_answer(vectorstore,self.question)

        # for doc in response["context"]:
        #     print(doc.page_content[:201])
        # print("----")

        ### Evaluate the answers
        faithfulness_check = faithfulness(response["context"],response['answer'])
        print(faithfulness_check)
        # answer_relevancy()
        relevancy_score = context_relevancy(self.question,response['answer'])
        print(relevancy_score)


# RAG(folder_path,"What is Bitcoin mining")
