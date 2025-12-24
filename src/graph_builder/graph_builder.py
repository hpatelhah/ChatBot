# Workflow Designs:

#basic: start >>> retriever >>> generator >>> end
#ReACT: start >>> retriever >>> generator with tools >>> end


from langgraph.graph import StateGraph, END, START
from state.state import State


class GraphBuilder:
    """Build Langgraph workflow"""

    def __init__(self, retriever, llm):

        self.retriever = retriever
        self.llm = llm
        self.nodes = None
        self.edges = None


    def build(self):
        builder = StateGraph(RAGState)

        builder.add_node()