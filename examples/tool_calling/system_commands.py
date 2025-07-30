# a function returning None will loop to input again whereas returning shared will forward to next step

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