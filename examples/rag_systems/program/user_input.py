from broverse import Action

class UserInput(Action):
    def run(self, shared):
        user_input = input("You: ")
        # print("You:", user_input)
        shared['user_input'] = user_input
        action = 'farewell' if user_input.lower() == 'exit' else 'router'
        shared['action'] = action
        return shared