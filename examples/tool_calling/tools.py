def add(a:int, b:int, **kwargs):
    """This function can add two numbers together"""
    result = a+b
    print(f"a+b is: {a}+{b}={result}")
    return result

def clear_user_input(shared:dict, **kwargs):
    """Clear user input"""
    shared['user_input'] = ''
    print("user_input is cleared")
    return None

def clear_chat_session(shared:dict, **kwargs):
    """Clear a chat session and remove/delete messages"""
    shared['messages'] = []
    print("session is cleared")
    return None

def save_memo(memo:str, **kwargs):
    """When users say `remember it`, `don't forget` or `remind me`, read all the input carefully, then summarize it and save them."""
    print(f"memo is saved: {memo}")
    with open("examples/tool_calling/prompts/memo.md", "w") as f:
        f.write(memo)
    return memo

def add_appointment(appointment_name:str, year:int, month:int, day:int, **kwargs):
    """Add an appointment on calendar when users show some intents such as add/create an appointment"""
    app_str = f"topic: {appointment_name}\nDate: {year:04d}-{month:02d}-{day:02d}"
    print(app_str)
    return app_str