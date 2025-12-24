from pydantic import BaseModel, Field


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



class SQLQuery(BaseModel):
    question: str = Field(
        description="Rewritten / clarified version of the user's question"
    )
    sql: str = Field(
        description="Executable SQL query that answers the question"
    )

