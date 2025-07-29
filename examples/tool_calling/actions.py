from broverse import Action, ModelInterface
import inspect
import typing
from typing import get_type_hints
import yaml, json

class Input(Action):
    def run(self, shared):
        user_input = input("You: ")
        shared['user_input'] = user_input
        shared['action'] = 'continue'
        return shared
    
class SystemCommand(Action):
    def __init__(self, ):
        super().__init__()
        self.commands = [
            f"/{command}"
            for command
            in ["clear_user_input", "clear_chat_session","exit", "list"]
        ]
    def get_slash_command(self, user_input:str):
        if user_input.startswith('/clear_user_input'):
            return 'clear_user_input'
        if user_input.startswith('/clear_chat_session'):
            return 'clear_chat_session'
        if user_input.startswith('/exit'):
            return 'end'
        if user_input.startswith('/list'):
            print("Available commands are:")
            for command in self.commands:
                print(f"\t- {command}")
            return 'continue'
        return 'continue'
    
    def run(self, shared):
        user_input = shared.get('user_input', 'no input')
        action = self.get_slash_command(user_input)
        if action == 'end':
            shared['action'] = 'end'
        elif action != 'continue':
            shared['tool'] = action
            shared['action'] = 'system_command'
        else:
            shared['action'] = 'continue'
        return shared

class ToolSelector(Action):
    def __init__(self, system_prompt:str, model:ModelInterface, tools:dict):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools

    def format_tools_for_selector(self):
        """Extract only tool name and description for ToolSelector"""
        formatted = []
        for name, tool_info in self.tools.items():
            description = tool_info['definition']['description']
            formatted.append(f"{name}: {description}")
        return formatted
    
    def convert_tool_str_to_dict(self, tool, codeblock='json'):
        tool = tool.split("```"+codeblock)
        if len(tool)>1:
            tool = tool[1]
        else:
            tool = tool[-1]
        tool = tool.split("```")[0].strip()
        print("Selected Tool: ", tool)
        if codeblock=='json':
            return json.loads(tool)
        return yaml.safe_load(tool)
    
    def run(self, shared):
        user_input = shared.get("user_input", "")
        tool_list = self.format_tools_for_selector()
        tool_list = "\t- ".join(tool_list)
        prompt = f"USER_INPUT: \n\n{user_input}\n\n"
        tool = self.model.run(
            system_prompt=self.system_prompt.format(tools=tool_list),
            messages=[self.model.UserMessage(text=prompt)]
        )
        print(tool)
        tool = self.convert_tool_str_to_dict(tool, codeblock='yaml')
        tool = tool.get('tool', None) if isinstance(tool, dict) else None
        shared['tool'] = tool
        shared['action'] = 'tool calling' if tool in self.tools else 'chat'
        
        return shared

class Tools(Action):
    def __init__(self, system_prompt:str, model:ModelInterface, tools:list):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        self.tools = self.register_tools(tools)

    def convert_to_tool(self, func)->dict:
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }

        for name, param in sig.parameters.items():
            param_type = type_hints.get(name, str)
            param_schema = {"type": self.python_type_to_json_type(param_type)}
            parameters["properties"][name] = param_schema
            if param.default is param.empty:
                parameters["required"].append(name)

        tool = {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": parameters
        }

        return tool


    def python_type_to_json_type(self, py_type):
        origin = typing.get_origin(py_type) or py_type

        if origin in [int]:
            return "integer"
        elif origin in [float]:
            return "number"
        elif origin in [bool]:
            return "boolean"
        elif origin in [str]:
            return "string"
        elif origin in [list, tuple]:
            return "array"
        elif origin in [dict]:
            return "object"
        else:
            return "string"  # fallback
        
    def get_params(self, tool):
        return self.convert_to_tool(tool)
        
    def register_tools(self, tools):
        _tools = {}
        for tool, action in tools:
            tool_definition = self.get_params(tool)
            name = tool_definition.get("name", None)
            _tools[name] = {
                "definition": tool_definition,
                "tool": tool,
                "action": action
            }
        return _tools

    def parse_str_to_json(self, params):
        params = params.split("```json")
        if len(params)>1:
            params = params[1]
        else:
            params = params[0]
        params = params.split("```")[0]
        return json.loads(params)
        
    def run(self, shared):
        user_input = shared.get('user_input', 'no input')
        tool_name = shared.get('tool', 'no tool')
        tool = self.tools.get(tool_name, {})
        definition = tool.get('definition', None)
        action = tool.get('action', None)
        tool = tool.get('tool', None)
        prompt = f"USER_INPUT: \n\n{user_input}\n\n"
        params = self.model.run(
            system_prompt=self.system_prompt.format(definition=json.dumps(definition)), 
            messages=[self.model.UserMessage(text=prompt)]
            )
        params = self.parse_str_to_json(params)
        if "shared" in params:
            params.pop("shared")
        response = tool(shared=shared, **params)
        print(f"AI: user_input = {user_input} | tool = {tool_name} | result = {response}")
        shared['tool_res'] = response
        shared['action'] = action
        return shared

class Chat(Action):
    def __init__(self, system_prompt, model:ModelInterface):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        if "messages" not in shared:
            shared["messages"] = []
        user_input = shared.get('user_input', 'no input')
        tool_res = shared.get('tool_res', None)
        context = f"CONTEXT: \n\n{tool_res}\n\n" if tool_res else ""
        message = f"{context}{user_input}".strip()
        shared["messages"].append(self.model.UserMessage(text=message))
        ai_response = self.model.run(
            system_prompt=self.system_prompt,
            messages=shared["messages"]
        )
        shared["messages"].append(self.model.AIMessage(text=ai_response))
        print(f"AI: {ai_response}")
        shared['action'] = 'continue'
        return shared