# a function returning None will loop to input again whereas returning shared will forward to next step

from brollm import BedrockChat

def exit(shared:dict):
    """Exit the program"""
    print("exit")
    return None

def clear(shared:dict):
    """Clear a chat session and remove/delete messages"""
    shared['messages'] = []
    print("session is cleared")
    return shared

def show_messages(shared:dict):
    """List all chat messages"""
    print("-"*20)
    print("MESSAGES HISTORY")
    messages = shared.get('messages', None)
    if messages:
        for message in messages:
            role = message['role']
            content = message['content'][0]['text']
            print(f"\t- {role}: {content}")
    else:
        print("<EMPTY>")
    print("-"*20)
    return shared

def save_memo(shared:dict)->dict:
    """Save your chat as a memo"""
    user_input = shared.get('user_input', 'empty')
    user_input = user_input.split(" ")    
    messages = shared.get('messages', []).copy()
    model = BedrockChat()
    if len(messages)==0 and len(user_input)==1:
        print("No messages to save")
        return shared
    summary = model.run(
        system_prompt=f"You're a helpful assistant. Do as a user says.", 
        messages=messages+[model.UserMessage(text=f"USER: {user_input}")]
    )
    with open("examples/tool_calling/prompts/memo.md", "w") as f:
        f.write(summary)
    print(f"memo is saved: {summary}")
    return shared