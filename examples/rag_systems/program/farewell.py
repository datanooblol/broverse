from broflow import Action
from bedrock import BedrockChat

class Farewell(Action):
    def __init__(self, system_prompt:str, model:BedrockChat):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        if "messages" not in shared:
            shared["messages"] = []
        input_message = shared.get("input", "No message")
        shared["messages"].append(self.model.UserMessage(text=f"{input_message}\n\nI gotta go now. See ya next time."))
        ai_response = self.model.run(self.system_prompt, shared["messages"])
        shared["messages"].append(self.model.AIMessage(text=ai_response))
        print("AI:", ai_response)
        shared["action"] = "end"
        return shared