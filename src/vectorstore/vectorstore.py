import sys, os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from langchain_core.documents import Document
from config.config import EMBEDDING_MODEL,RETRIEVER_SEARCH_TYPE,RETRIEVER_K 

class VectorStore:
    "Manages vector store applications"
    def __init__(self, model_id=EMBEDDING_MODEL, docs=None, retriever_search_type=RETRIEVER_SEARCH_TYPE,k=RETRIEVER_K):
        self.model_id = model_id
        self.embeddings = BedrockEmbeddings(model_id=model_id)
        self.retriever_search_type = retriever_search_type
        self.k = k
        self.vectorstore = None
        self.retriever = None
        if docs:
            self.create_retriever(docs, self.retriever_search_type, self.k)


    def create_retriever(self, docs, retriever_search_type=RETRIEVER_SEARCH_TYPE,k=RETRIEVER_K):
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_type= retriever_search_type, search_kwarg={'k': k})

    def get_retriever(self):

        if self.retriever is None:
            print("run create_retriever(docs) method first")
        else:
            return self.retriever
            
    def retrieve(self, query: str):
        if self.retriever is None:
            print("run create_retriever(docs) method first")
        else:
            return self.retriever.invoke(query)

        
