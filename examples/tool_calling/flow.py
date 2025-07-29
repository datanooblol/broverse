from actions import Tools, ToolSelector, Input, SystemCommand, Chat
from tools import add, clear_user_input, clear_chat_session, save_memo, add_appointment
from prompts.system_prompts import tool_selector_prompt, tool_prompt
from broverse import Start, End, Flow
from broverse.bedrock import BedrockChat

def get_flow():
    start_action = Start(message="Start Flow", next_action="input")
    input_action = Input()
    system_command_action = SystemCommand()
    chat_action = Chat(
        system_prompt="You are a helpful assistant",
        model=BedrockChat()
    )
    with open("examples/tool_calling/prompts/tool_call.yaml", "r") as f:
        tool_prompt = f.read()    
    tools = Tools(
        system_prompt=tool_prompt,
        model=BedrockChat(),
        tools=[
            (clear_user_input, 'continue'),
            (clear_chat_session, 'continue'),
            (add, 'chat'),
            (save_memo, 'chat'),
            (add_appointment, 'chat')
        ]
    )
    with open("examples/tool_calling/prompts/tool_selector.yaml", "r") as f:
        tool_selector_prompt = f.read()
    tool_selector_action = ToolSelector(
        system_prompt=tool_selector_prompt,
        model=BedrockChat(),
        tools=tools.tools
    )
    end_action = End(message="End Flow")

    start_action - "input" >> input_action
    input_action - "continue" >> system_command_action
    system_command_action - "continue" >> tool_selector_action
    tool_selector_action - "tool calling" >> tools
    tool_selector_action - "chat" >> chat_action
    system_command_action - "system_command" >> tools
    tools - "chat" >> chat_action
    tools - "continue" >> input_action
    chat_action - "continue" >> input_action
    system_command_action - "end" >> end_action

    flow = Flow(start_action=start_action)
    return flow