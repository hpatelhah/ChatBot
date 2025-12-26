from abc import ABC, abstractmethod
from langchain_community.tools.tavily_search import TavilySearchResults
from state.state import State
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from vectorstore.vectorstore import VectorStore
from prompt.prompt import SQL_PROMPT


class Node(ABC):
    def __init__(self, name, state=None, prompt=None):
        self.name = name
        self.state = State
        self.prompt = prompt



class InputNode(Node):
    def run(self, name, input_data, state: State):
        self.name = name
        self.input_data = input_data
        self.state = state 


class SQLNode(Node):
    
    def run(self, input_data, state: State, llm, prompt=SQL_PROMPT):

        return llm.invoke(SQL_PROMPT.with_inputs(**input_data))

        
        
class PromptNode(Node):

    def __init__(name, state, prompt):
        super.__init__(name, state)
        self.prompt = prompt
    def run(self, prompt):
        pass

class RAGNode(Node):
    def __init__(self, name,  state, vectorstore: VectorStore ,input_query=None, llm=None):
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
        