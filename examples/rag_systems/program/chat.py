from broflow import Action
from bedrock import BedrockChat
class Chat(Action):
    def __init__(self, system_prompt, model:BedrockChat):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        user_input = shared.get("user_input", "No input")
        if "messages" not in shared:
            shared["messages"] = []
        shared["messages"].append(self.model.UserMessage(text=user_input))
        ai_response = self.model.run(system_prompt=self.system_prompt, messages=shared["messages"])
        print("AI:", ai_response)
        shared["messages"].append(self.model.AIMessage(text=ai_response))
        shared["action"] = "continue"
        return shared