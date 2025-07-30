def save_memo(memo:str, **kwargs):
    """When users say `remember it`, `don't forget` or `remind me`, read all the input carefully, then summarize it and save them."""
    print(f"memo is saved: {memo}")
    with open("examples/tool_calling/prompts/memo.md", "w") as f:
        f.write(memo)
    return memo

def add_appointment(event_name:str, year:int, month:int, day:int, **kwargs):
    """Add an appointment on calendar when users show some intents such as add/create an appointment"""
    app_str = f"Event: {event_name}\nDate: {year:04d}-{month:02d}-{day:02d}"
    print(app_str)
    return app_str