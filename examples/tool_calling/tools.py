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