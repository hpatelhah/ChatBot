import sys
import os

print("Python executable:", sys.executable)
print("sys.path:", sys.path)


from llm.llm import AWSBedrockLLm
from nodes.nodes import SQLNode
from state.state import State
from vectorstore.vectorstore import VectorStore
from documents.schema import all_docs

llm = AWSBedrockLLm()

state = State()

vectorstore = VectorStore(docs=all_docs)

usersql = 'whats client count for last month by state?'
usergeneral = 'what is capital of USA?'
usergoogle = 'what are top 2025 NYE events in NYC?'

sqlnode1 = SQLNode('sqlnode1')
sqlnode1_run = sqlnode1.run( 
{'docs': vectorstore.retrieve(usersql), 'query': usersql}, 
state, llm  )

print(sqlnode1_run)
