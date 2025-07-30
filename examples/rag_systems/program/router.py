from broverse import Action
from broverse.bedrock import BedrockChat
import yaml

class Router(Action):
    def __init__(self, system_prompt, model:BedrockChat):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def get_action(self, intent):
        if intent == "farewell":
            return "farewell"
        else:
            return "chat"

    def run(self, shared):
        user_input = shared.get("user_input", "No input")
        intent = self.model.run(system_prompt=self.system_prompt, messages=[self.model.UserMessage(text=user_input)])
        intent = intent.split("```yaml")[1].split("```")[0].strip()
        intent = yaml.safe_load(intent)["action"]
        print("USER INTENT:", intent)
        shared['action'] = self.get_action(intent)
        return shared