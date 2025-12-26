from pydantic import BaseModel, Field


class SQLQuery(BaseModel):
    question: str = Field(
        description="Rewritten / clarified version of the user's question"
    )
    sql: str = Field(
        description="Executable SQL query that answers the question"
    )
