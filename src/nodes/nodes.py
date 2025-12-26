from abc import ABC, abstractmethod
from langchain_community.tools.tavily_search import TavilySearchResults
from state.state import State
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from vectorstore.vectorstore import VectorStore
from prompt.prompt import SQL_PROMPT
from util import format_docs

# node design = input data, state (for history), output
# utils required to perform task - llm, reteriver, tools
# not all nodes require all utils

class Node(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs):
        pass



class InputNode(Node):
    def run(self, name, input_data, state: State):
        self.name = name
        self.input_data = input_data
        self.state = state 


class SQLNode(Node):

    def run(self, input_data, state, llm, prompt_template=SQL_PROMPT):       
        return llm.invoke(prompt_template.with_inputs(input_data))

        
        
class PromptNode(Node):

    def run(self, prompt, state, llm):
        return llm.invoke(prompt)

class RAGNode(Node):
    def __init__(self, name,  state, vectorstore: VectorStore ,input_query=None, llm=None):
        super().__init__(name, state)
        self.input = input_query
        self.vectorstore = vectorstore
        if self.input:
            self.query = self.input_query
        else:
            self.query = self.state.messages[-1]

    
    def run():
        retrieved_docs = self.retriever.retrieve(self.query)
        response
        