from broverse.action import BaseAction, Action
from typing import Dict, Any
import copy

class Flow(BaseAction):
    def __init__(self, start_action:Action):
        self.start_action:Action = start_action

    def run(self, shared:Dict[str, Any]):
        current_action = copy.copy(self.start_action)
        next_action_name = None
        while current_action:
            next_action_name = current_action.execute_action(shared)
            current_action = current_action.get_next_action(next_action_name)
        return next_action_name
    
    def to_mermaid(self):
        """Generate mermaid flowchart"""
        lines = ["```mermaid", "flowchart TD"]
        visited = set()
        
        def traverse(action:Action, action_name:str="start"):
            if id(action) in visited:
                return
            visited.add(id(action))
            
            for next_name, next_action in action.successors.items():
                next_action_name = next_action.__class__.__name__
                lines.append(f"    {action_name} -->|{next_name}| {next_action_name}")
                traverse(next_action, next_action_name)
        
        traverse(self.start_action, self.start_action.__class__.__name__)
        lines.append("```")
        return "\n".join(lines)
    
    def save_mermaid(self, filename):
        """Save mermaid chart to .md file"""
        with open(filename, 'w') as f:
            f.write(self.to_mermaid())