from typing import List
from pydantic import BaseModel
from langchain.schema import Document



class RAGState(BaseModel):
    """State object for rag workflow"""
    question: str
    retrieved_docs: List[Document]
    answer: str