import sys, os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from langchain_core.documents import Document
from config.config import EMBEDDING_MODEL,RETRIEVER_SEARCH_TYPE,RETRIEVER_K 

class VectorStore:
    "Manages vector store applications"
    def __init__(self):
        self.embeddings = BedrockEmbeddings(model=config.EMBEDDING_MODEL)
        self.vectorstore = None
        self.retriever = None

    def create_retriever(self, docs):
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_type= RETRIEVER_SEARCH_TYPE, kwarg={'k': RETRIEVER_K})

    def get_retriever(self):

        if self.retriever is None:
            print("run create_retriever(docs) method first")
        else:
            return self.retriever
            
    def retrieve(query: str):
        if self.retriever is None:
            print("run create_retriever(docs) method first")
        else:
            self.retriever.invoke(query)