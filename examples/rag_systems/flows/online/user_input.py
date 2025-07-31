from broflow import Action

class UserInput(Action):
    def __init__(self):
        super().__init__()
        self.commands = {
            "/help": "Show available commands",
            "/exit": "Exit the application",
            "/rag <query>": "using rag"
        }

    def quick_command(self, user_input:str):
        if not user_input.startswith("/"):
            return 'default'
        if user_input.startswith("/help"):
            for c, d in self.commands.items():
                print(f"{c}: {d}")
            return None
        if user_input.startswith("/exit"):
            return 'farewell'
        if user_input.startswith("/rag"):
            return 'rag'
        
    def run(self, shared):
        while True:
            user_input = input("You: ")
            action = self.quick_command(user_input.lower())
            if action:
                break
        shared['user_input'] = user_input
        self.next_action = action
        return shared