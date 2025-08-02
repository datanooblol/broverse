from broflow import Action
from brollm import BaseLLM
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Shared:
    user_input: Optional[str] = None
    messages: list = field(default_factory=list)

class Input(Action):
    def run(self, shared:Shared):
        user_input = input("Enter your input: ")
        shared.user_input = user_input
        return shared
    
class Thought(Action):
    def __init__(self, system_prompt:str, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        response = self.model.run(
            system_prompt=self.system_prompt,
            messages=[]
        )
        return shared
    
class ToolSelector(Action):
    def __init__(self, system_prompt:str, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        response = self.model.run(
            system_prompt=self.system_prompt,
            messages=[]
        )
        return shared
    
class ToolRunner(Action):
    def __init__(self, system_prompt:str, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        response = self.model.run(
            system_prompt=self.system_prompt,
            messages=[]
        )
        return shared
    
class Router(Action):
    def __init__(self, system_prompt:str, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        response = self.model.run(
            system_prompt=self.system_prompt,
            messages=[]
        )
        return shared
    
class Chat(Action):
    def __init__(self, system_prompt:str, model:BaseLLM):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        response = self.model.run(
            system_prompt=self.system_prompt,
            messages=[]
        )
        return shared