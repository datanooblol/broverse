from broflow import Action, ModelInterface
import yaml, json
from broflow.tools import (
    generate_extract_parameters_prompt, 
    validate_parameters, 
    list_tools,
    parse_codeblock_to_dict
)
from typing import List, Callable

class Input(Action):
    def run(self, shared):
        user_input = input("You: ")
        shared['user_input'] = user_input
        return shared
    
class SystemCommand(Action):
    def __init__(self, tools:list):
        super().__init__()
        self.tools = tools

    def validate_system_command(self, shared:dict):
        user_input = shared.get('user_input', 'no input')
        if user_input.startswith('/') is False:
            return 'default'
        command = user_input.split(" ")[0]
        print(command)
        if command == "/list":
            print(f"COMMAND LIST:\n{list_tools(self.tools)}")
            return 'input'
        tool = [t for t in self.tools if f"/{t.__name__}" == command][0]
        return 'input' if tool(shared) else 'exit'
    
    def run(self, shared:dict):
        self.next_action = self.validate_system_command(shared)
        return shared
# class SystemCommand(Action):
#     def __init__(self, tools:dict):
#         super().__init__()
#         self.tools = tools
    
#     def validate_system_command(self, shared:dict):
#         user_input = shared.get('user_input', 'no input')
#         if user_input.startswith('/list'):
#             print('Command List')
#             for k, v in self.tools.items():
#                 print(f"\t- /{k}: {v['definition']['description']}")
#             return 'input'
#         if user_input.startswith('/'):
#             user_input = user_input.split(" ")[0]
#             user_input = user_input.replace("/", "")
#             tool = self.tools.get(user_input, {})
#             func = tool.get('tool', {})
#             return 'input' if func(shared) else 'exit'
#         return 'default'

#     def run(self, shared):
#         self.next_action = self.validate_system_command(shared)
#         return shared

class ToolSelector(Action):
    def __init__(self, system_prompt:str, model:ModelInterface, tools:List[Callable]):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools
    
    def fallback(self, prompt, tool_list):
        errors = []
        for i in range(5):
            try:
                tool = self.model.run(
                    system_prompt=self.system_prompt.format(tools=tool_list),
                    messages=[self.model.UserMessage(text=prompt+f"{errors}")]
                )
                tool = parse_codeblock_to_dict(tool, codeblock='yaml')
                return tool
            except Exception as e:
                errors.append(str(e))
        return None

    def run(self, shared):
        user_input = shared.get('user_input', 'no input')
        tool_list = list_tools(self.tools)
        prompt = f"USER_INPUT: \n\n{user_input}\n\n"
        tool = self.fallback(prompt, tool_list)
        self.print(tool)
        tool_name = tool.get('tool', None) if isinstance(tool, dict) else None
        shared['tool_name'] = tool_name
        self.print(tool_name)
        self.next_action = 'tool calling' if tool_name in [tool.__name__ for tool in self.tools] else 'chat'
        return shared

class Tools(Action):
    def __init__(self, model:ModelInterface, tools:List[Callable]):
        super().__init__()
        self.model = model
        self.tools = tools
    
    def fallback(self, system_prompt, user_input, tool):
        errors = []
        prompt = f"USER_INPUT: \n\n{user_input}\n\n"
        for i in range(5):
            try:
                parameters = self.model.run(
                    system_prompt=system_prompt,
                    messages=[self.model.UserMessage(text=f"{prompt} {errors}")]
                )
                parameters = parse_codeblock_to_dict(parameters, codeblock='yaml')
                response = tool(**parameters)
                return response
            except Exception as e:
                errors.append(str(e))
        return None

    def run(self, shared):
        user_input = shared.get('user_input', 'no input')
        tool_name = shared.get('tool_name', '')
        tool = [tool for tool in self.tools if tool.__name__ == tool_name][0]
        system_prompt = generate_extract_parameters_prompt(tool)
        response = self.fallback(system_prompt, user_input, tool)
        self.print(f"AI: user_input = {user_input} | tool = {tool_name} | result = {response}")
        shared['tool_res'] = response
        self.next_action = self.next_action if response else 'input'
        return shared

class Chat(Action):
    def __init__(self, system_prompt, model:ModelInterface):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        self.memo = "./examples/tool_calling/prompts/memo.md"

    def run(self, shared):
        if "messages" not in shared:
            shared['messages'] = []
        user_input = shared.get('user_input', 'no input')
        tool_res = shared.get('tool_res', None)
        context = f"CONTEXT: \n\n{tool_res}\n\n" if tool_res else ""
        with open(self.memo, "r") as f:
            memo = f.read()
        system_prompt = self.system_prompt if len(memo)==0 else f"{self.system_prompt}\n\nMEMO: \n\n{memo}\n\n"
        message = f"{context}{user_input}".strip()
        ai_response = self.model.run(
            system_prompt=system_prompt,
            messages=shared["messages"]+[self.model.UserMessage(text=message)]
        )
        shared["messages"].append(self.model.UserMessage(text=user_input))
        shared["messages"].append(self.model.AIMessage(text=ai_response))
        print(f"AI: {ai_response}")
        return shared