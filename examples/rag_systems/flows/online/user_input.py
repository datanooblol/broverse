from broflow import Action

class UserInput(Action):
    def run(self, shared):
        user_input = input("You: ")
        shared['user_input'] = user_input
        self.next_action = 'farewell' if user_input.lower() == '/exit' else 'default'
        return shared