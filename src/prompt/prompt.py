
from abc import ABC, abstractmethod
from langchain_core.prompts import PromptTemplate

# predefined basic prompts
SUMMARY_PROMPT = PromptTemplate.from_template("Summarize the following concisely focusing only on main points:{text}")

class Prompt(ABC):
    def __init__(self, inputs):
        self.inputs = inputs

    def prompt():
        pass

class CustomPrompt():
    def __init__(self, template):
        self.template = PromptTemplate.from_template(template)

    def get(self, input_data:dict):
        return self.template.format(**input_data)


# usage
test = CustomPrompt("summarize this {text}")
formatted = test.get({"text": "HI"})
print(formatted)

print(SUMMARY_PROMPT.format(text="HII"))




