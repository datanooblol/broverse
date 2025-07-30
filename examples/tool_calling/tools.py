from broverse.bedrock import BedrockChat

def save_memo(user_input:str, **kwargs)->None:
    """
    <|start|>
        Use this tool when user's intent is about to save this and discuss it later on. 
        Do not confuse when user asks about the memo because it's not about saving.
    <|end|>
    Args:
        user_input (str) : the whole user input
    Return:
        str : a short summary of what user says
    """
    model = BedrockChat()
    summary = model.run(system_prompt="Summarize what user says as comprehensive as possible", messages=[model.UserMessage(text=user_input)])
    with open("examples/tool_calling/prompts/memo.md", "w") as f:
        f.write(summary)
    print(f"memo is saved: {summary}")
    return None

def add_appointment(event_name:str, year:int, month:int, day:int, **kwargs)->str:
    """
    <|start|>
        Add an appointment on calendar when users show some intents such as add/create an appointment
    <|end|>
    
    Args:
        event (str) : the meaningful name of event
        year (int) : the year of the event
        month (int) : the month of the event
        day (int) : the day of the event
    
    Return:
        str        
    """
    app_str = f"Event: {event_name}\nDate: {year:04d}-{month:02d}-{day:02d}"
    print(app_str)
    return app_str