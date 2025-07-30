from broverse import Action, ModelInterface
import yaml, json

class Input(Action):
    def run(self, shared):
        user_input = input("You: ")
        shared['user_input'] = user_input
        if "messages" not in shared:
            shared['messages'] = []
        return shared

class SystemCommand(Action):
    def __init__(self, tools:dict):
        super().__init__()
        self.tools = tools
    
    def validate_system_command(self, shared:dict):
        user_input = shared.get('user_input', 'no input')
        if user_input.startswith('/list'):
            print('Command List')
            for k, v in self.tools.items():
                print(f"\t- /{k}: {v['definition']['description']}")
            return 'input'
        if user_input.startswith('/'):
            user_input = user_input.split(" ")[0]
            user_input = user_input.replace("/", "")
            tool = self.tools.get(user_input, {})
            func = tool.get('tool', {})
            return 'input' if func(shared) else 'exit'
        return 'default'

    def run(self, shared):
        self.next_action = self.validate_system_command(shared)
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
        # print("Selected Tool: ", tool)
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
        tool = self.convert_tool_str_to_dict(tool, codeblock='yaml')
        self.print(tool)
        tool = tool.get('tool', None) if isinstance(tool, dict) else None
        shared['tool'] = tool
        self.next_action = 'tool calling' if tool in self.tools else 'chat'
        return shared

class Tools(Action):
    def __init__(self, system_prompt:str, model:ModelInterface, tools:dict):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools

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
        return shared

class Chat(Action):
    def __init__(self, system_prompt, model:ModelInterface):
        super().__init__()
        self.system_prompt = system_prompt
        self.model = model

    def run(self, shared):
        user_input = shared.get('user_input', 'no input')
        tool_res = shared.get('tool_res', None)
        context = f"CONTEXT: \n\n{tool_res}\n\n" if tool_res else ""
        message = f"{context}{user_input}".strip()
        ai_response = self.model.run(
            system_prompt=self.system_prompt,
            messages=shared["messages"]+[self.model.UserMessage(text=message)]
        )
        shared["messages"].append(self.model.UserMessage(text=user_input))
        shared["messages"].append(self.model.AIMessage(text=ai_response))
        print(f"AI: {ai_response}")
        return shared