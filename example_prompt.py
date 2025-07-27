from broverse import Prompt, PromptAction, Flow

# Create a prompt easily
prompt = Prompt(
    persona="You are a helpful coding assistant",
    instructions="Help the user write clean Python code",
    cautions="Always validate input parameters",
    structured_output="Return code in markdown format"
).add_example("Input: 'hello world'\nOutput: ```python\nprint('hello world')\n```")

# Use in an action
class CodeAction(PromptAction):
    def run(self, shared):
        prompt_text = self.prompt.format(**shared)
        # Here you'd call your AI service with prompt_text
        return f"Generated code for: {shared.get('task', 'unknown')}"

# Use in a flow
action = CodeAction(prompt)
flow = Flow(action)

# Run it
result = flow.run({"task": "create a function"})
print(result)