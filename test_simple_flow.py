from broverse.action import Action
from broverse.flow import Flow
from broverse.bedrock import BedrockChat
from typing import Any
import yaml
import os

class InputAction(Action):
    def run(self, shared):
        message = input("You: ")
        shared['input'] = message
        return message

    def validate_next_action(self, inputs: Any) -> str:
        if "exit" == inputs.lower():
            return "end"
        return "router"
    
class RouterAction(Action):
    def __init__(self, system_prompt:str, model:BedrockChat):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        input_message = shared.get("input", "No message")
        intent = self.model.run(self.system_prompt, [self.model.UserMessage(text=input_message)])
        intent = intent.split("```yaml")[1].split("```")[0].strip()
        intent = yaml.safe_load(intent)['action']
        print("Intent:", intent)
        return intent
    
    def validate_next_action(self, inputs:Any) -> str:
        if inputs == 'farewell':
            return 'farewell'
        return "chat"

class ChatAction(Action):
    def __init__(self, system_prompt:str, model:BedrockChat):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
    
    def run(self, shared):
        if "messages" not in shared:
            shared["messages"] = []
        input_message = shared.get("input", "No message")
        shared["messages"].append(self.model.UserMessage(text=input_message))
        ai_response = self.model.run(self.system_prompt, shared["messages"])
        shared["messages"].append(self.model.AIMessage(text=ai_response))
        print("AI:", ai_response)
        return ai_response
    
    def validate_next_action(self, inputs: Any) -> str:
        return "continue"
    
class FarewellAction(Action):
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
        return ai_response
    
    def validate_next_action(self, inputs: Any) -> str:
        return "end"

class End(Action):
    def run(self, shared):
        return None
    
router_prompt = """\
classify a user's intent based on the input messages. 
Intent options are:
1. continue if nothing goes wrong
2. farewell if a user's message indicate that he or she wants to go somewhere

Return your response in codeblock with this following yaml format:
```yaml
action: either continue or farewell
```

IMPORTANT: Make sure to:
1. Use proper indentation (4 spaces) for all multi-line fields
2. Use the | character for multi-line text fields
3. Keep single-line fields without the | character
""".strip()

if __name__=='__main__':

    input_action = InputAction()
    chat_action = ChatAction(
        system_prompt="You are a helpful assistant",
        model=BedrockChat()
    )
    router_action = RouterAction(
        system_prompt=router_prompt,
        model=BedrockChat()
    )

    farewell_action = FarewellAction(
        system_prompt="Your job is to farewell a user.",
        model=BedrockChat()
    )
    
    input_action -"router">> router_action
    router_action -"chat">> chat_action
    router_action -"farewell">> farewell_action
    chat_action -"continue">> input_action

    for action in [input_action, farewell_action]:
        action -"end">> End()

    flow = Flow(start_action=input_action)
    filename = os.path.basename(__file__).replace(".py", ".md")
    flow.save_mermaid(filename=filename)
    shared = {}
    flow.run(shared=shared)    