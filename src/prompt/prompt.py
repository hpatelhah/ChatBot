
from abc import ABC, abstractmethod
from langchain_core.prompts import PromptTemplate

# predefined basic prompts

class Prompt(ABC):
    def __init__(self, inputs):
        self.inputs = inputs

    def prompt():
        pass

class CustomPrompt():
    def __init__(self, template):
        self.template = PromptTemplate.from_template(template)

    def with_inputs(self, input_data:dict):
        return self.template.format_prompt(**input_data)



SUMMARY_PROMPT = CustomPrompt("Summarize the following concisely focusing only on main points:{text}")
SQL_PROMPT = CustomPrompt("""You are a SQL expert, generate an executable postgres sql 
based on the retireved docs and user question.\n Context docs: {docs} \n User question: {query}""")

# usage
#test = CustomPrompt("summarize this {text}")
#formatted = test.get({"text": "HI"})
#print(formatted)

#print(SUMMARY_PROMPT.format(text="HII"))




