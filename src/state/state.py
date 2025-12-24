from typing import List, Annotated, TypedDict, Sequence
from pydantic import BaseModel
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
  