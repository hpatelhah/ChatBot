from abc import ABC, abstractmethod
#from state.rag_state import State
from langchain_community.tools.tavily_search import TavilySearchResults
from state.state import State
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from vectorstore.vectorstore import VectorStore


class Node(ABC):
    def __init__(self, name, state:State, prompt=None):
        self.name = name
        self.state = State
        self.prompt = prompt



class InputNode(Node):
    def run(self, input_data, state: State):
        self.input_data = input_data
        self.state = state 


class SQLNode(Node):
    def run(self, input_data, state: State):
        pass
        
class PromptNode(Node):

    def __init__(name, state, prompt):
        super.__init__(name, state)
        self.prompt = prompt
    def run(self, prompt):
        pass

class RAGNode(Node):
    def __init__(self, name,  state: State, vectorstore: VectorStore ,input_query=None, llm=None):
        super().__init__(name, state)
        self.input = input_query
        self.vectorstore = vectorstore
        self.llm = llm
        if self.input:
            self.query = self.input_query
        else:
            self.query = self.state.messages[-1]

    
    def run():
        retrieved_docs = self.retriever.retrieve(self.query)
        response
        