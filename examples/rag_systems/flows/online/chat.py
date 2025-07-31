from broflow import Action
from brollm import BedrockChat

class Chat(Action):
    def __init__(self, system_prompt, model:BedrockChat):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
    def create_context(self, contexts):
        return "\n\n".join([f"{c.context}" for c in contexts])
    
    def run(self, shared):
        user_input = shared.get("user_input", "No input")
        if "messages" not in shared:
            shared["messages"] = []
        if "contexts" in shared:
            contexts = shared.pop('contexts')
            prompt = "CONTEXT:\n\n{contexts}\n\nBased on CONTEXT above, {user_input}".format(
                    contexts=self.create_context(contexts),
                    user_input=user_input
                )
            self.print(prompt)
        else:
            prompt = user_input
        ai_response = self.model.run(system_prompt=self.system_prompt, messages=shared["messages"]+[self.model.UserMessage(text=prompt)])
        shared["messages"].append(self.model.UserMessage(text=user_input))
        print("AI:", ai_response)
        shared["messages"].append(self.model.AIMessage(text=ai_response))
        return shared