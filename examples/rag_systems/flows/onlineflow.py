from broverse.program import UserInput, Router, Chat, Farewell
from broverse.bedrock import BedrockChat
from broverse import End, Flow

chat_system_prompt = """\
You are an AI assistant.
""".strip()

farewell_system_prompt = """\
Your job is to farewell a user.
""".strip()

router_system_prompt = """\
Classify a user's intent based on the input messages. 
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

def get_online_flow():
    user_input_action = UserInput()
    router_action = Router(
        system_prompt=router_system_prompt,
        model=BedrockChat()
    )
    chat_action = Chat(
        system_prompt=chat_system_prompt,
        model=BedrockChat()
    )
    farewell = Farewell(
        system_prompt=farewell_system_prompt,
        model=BedrockChat()
    )
    end = End(message="End of Online Flow")

    user_input_action - "router" >> router_action
    router_action - "chat" >> chat_action
    user_input_action - "farewell" >> farewell
    router_action - "farewell" >> farewell
    chat_action - "continue" >> user_input_action
    farewell - "end" >> end
    
    flow = Flow(start_action=user_input_action)
    return flow