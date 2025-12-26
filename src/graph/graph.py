# Workflow Designs:

#basic: start >>> retriever >>> generator >>> end
#ReACT: start >>> retriever >>> generator with tools >>> end


from langgraph.graph import StateGraph, END, START
from state.state import State


class Graph:
    """Build Langgraph workflow"""

    def __init__(self, statetype, nodes, regular_edges, conditional_edges=None):

        self.nodes = []
        self.edges = []
        self.statetype = statetype
        self.graph = build()

    def add_nodes(self, nodes: List):
        self.nodes = self.nodes + nodes

    def add_edges(self, edges: List):
        self.edges = self.edges + edges
    
    def build(self):
        builder = StateGraph(State)


    def build(self):
        builder = StateGraph(self.state)

        builder