from broverse.action import Action
from broverse.prompt import Prompt
from typing import Dict, Any

class PromptAction(Action):
    """Action that uses a Prompt for AI agent interactions"""
    
    def __init__(self, prompt: Prompt):
        super().__init__()
        self.prompt = prompt
    
    def run(self, shared: Dict[str, Any]) -> Any:
        """Override this to implement your AI agent call"""
        prompt_text = self.prompt.format(**shared)
        # This is where you'd call your AI service
        # For now, just return the formatted prompt
        return prompt_text