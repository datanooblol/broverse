from .online.chat import Chat
from .online.farewell import Farewell
from .online.router import Router
from .online.user_input import UserInput
from brollm import BedrockChat
from broflow import Start, End, Flow
from broflow import load_prompt_yaml
from broflow import load_config

def get_online_flow():
    prompt_dir = 'examples/rag_systems/prompts'
    load_config('examples/rag_systems/config.yml')
    start_action = Start(message="Start of Online Flow")
    user_input_action = UserInput()
    router_action = Router(
        system_prompt=load_prompt_yaml(f'{prompt_dir}/router.yml'),
        model=BedrockChat()
    )
    chat_action = Chat(
        system_prompt=load_prompt_yaml(f'{prompt_dir}/chat.yml'),
        model=BedrockChat()
    )
    farewell_action = Farewell(
        system_prompt=load_prompt_yaml(f'{prompt_dir}/farewell.yml'),
        model=BedrockChat()
    )
    end_action = End(message="End of Online Flow")

    start_action >> user_input_action >> router_action >> chat_action >> user_input_action
    user_input_action -"farewell" >> farewell_action
    router_action - "farewell" >> farewell_action >> end_action
    
    flow = Flow(start_action=start_action, name="Online Flow")
    return flow