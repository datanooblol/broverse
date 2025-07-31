from broflow import Action
from broflow import parse_codeblock_to_dict
from brollm import BedrockChat

class Router(Action):
    def __init__(self, system_prompt, model:BedrockChat):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def get_action(self, intent):
        if intent == "farewell":
            return "farewell"
        else:
            return "default"
    
    def fallback(self, shared):
        user_input = shared.get("user_input", "No input")
        errors = []
        for i in range(5):
            try:
                prompt = user_input if len(errors)==0 else "{user_input}\n\nAvoid below errors:\n\n{errors}".format(user_input=user_input, errors="\n".join(errors))
                intent = self.model.run(system_prompt=self.system_prompt, messages=[self.model.UserMessage(text=prompt)])
                self.print("USER INTENT: {intent}".format(intent=intent))
                intent = parse_codeblock_to_dict(intent, codeblock='yaml')
                intent = intent.get('action', None)
                return intent
            except Exception as e:
                errors.append(str(e))
                self.print("Routing error: {e}".format(e=str(e)))
        return None
    
    def run(self, shared):
        intent = self.fallback(shared)
        self.next_action = self.get_action(intent)
        return shared