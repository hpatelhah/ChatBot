from langchain_aws import ChatBedrockConverse

class AWSBedrockLLm():
    
    def __init__(self, model_id, structured_output=None):
        self.model_id = model_id
        self.model = ChatBedrockConverse(model=self.model_id)
        self.structured_output_schema = structured_output
        if structured_output:
            self.model = self.model.with_structured_output(structured_output)

    def invoke(self, query):
        return self.model.invoke(query)

    


