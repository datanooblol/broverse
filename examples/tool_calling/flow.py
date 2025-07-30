from actions import Tools, ToolSelector, Input, SystemCommand, Chat
from tools import save_memo, add_appointment
from system_commands import clear, exit, show_messages
from broverse import Start, End, Flow
from broverse.tools import register_tools
from broverse.bedrock import BedrockChat
from broverse import load_config

def get_flow():
    load_config("examples/tool_calling/config.yaml")
    system_commands = [clear, exit, show_messages]
    system_tools = [save_memo, add_appointment]
    start_action = Start(message="Start Flow")
    input_action = Input()
    system_command_action = SystemCommand(
        tools=system_commands
    )
    chat_action = Chat(
        system_prompt="You are a helpful assistant",
        model=BedrockChat()
    )
    tools = Tools(
        model=BedrockChat(),
        tools=system_tools
    )
    with open("examples/tool_calling/prompts/tool_selector.yaml", "r") as f:
        tool_selector_prompt = f.read()
    tool_selector_action = ToolSelector(
        system_prompt=tool_selector_prompt,
        model=BedrockChat(),
        tools=system_tools
    )
    end_action = End(message="End Flow")

    start_action >> input_action >> system_command_action
    system_command_action - "input" >> input_action
    system_command_action - "exit" >> end_action
    system_command_action >> tool_selector_action
    tool_selector_action - "tool calling" >> tools >> chat_action
    tools - "input" >> input_action
    tool_selector_action - "chat" >> chat_action
    chat_action >> input_action

    flow = Flow(start_action=start_action)
    return flow