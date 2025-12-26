
from llm.llm import AWSBedrockLLm
from nodes.nodes import SQLNode, PromptNode
from state.state import State
from vectorstore.vectorstore import VectorStore
from documents.schema import all_docs
from util import format_docs
from parser.parser import SQLQuery
llm = AWSBedrockLLm()
llm_structure = AWSBedrockLLm(structured_output=SQLQuery)
state = State()

vectorstore = VectorStore(docs=all_docs)

usersql = 'whats client count for last month by state?'
usergeneral = 'what is capital of USA?'
usergoogle = 'what are top 2025 NYE events in NYC?'

sqlnode1 = SQLNode('sqlnode1')
docs = format_docs(vectorstore.retrieve(usersql))
d = {'docs': docs, 'query': usersql}
sqlnode1_run = sqlnode1.run(d, state, llm_structure  )

print(sqlnode1_run.sql)


promptnode1 = PromptNode('promptnode1')
promptnode1_run = promptnode1.run(usergeneral, state, llm )
print(promptnode1_run)

