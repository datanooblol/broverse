from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class Prompt:
    persona: str = ""
    instructions: str = ""
    cautions: str = ""
    structured_output: str = ""
    examples: List[str] = field(default_factory=list)
    
    def __post_init__(self, **kwargs):
        # Silently ignore extra keywords
        pass
    
    def __str__(self) -> str:
        """Generate the complete prompt string"""
        parts = []
        
        if self.persona:
            parts.append(f"# Persona\n{self.persona}")
        
        if self.instructions:
            parts.append(f"# Instructions\n{self.instructions}")
        
        if self.cautions:
            parts.append(f"# Cautions\n{self.cautions}")
        
        if self.structured_output:
            parts.append(f"# Structured Output\n{self.structured_output}")
        
        if self.examples:
            parts.append("# Examples")
            for i, example in enumerate(self.examples, 1):
                parts.append(f"## Example {i}\n{example}")
        
        return "\n\n".join(parts)
    
    def add_example(self, example: str) -> 'Prompt':
        """Add an example and return self for chaining"""
        self.examples.append(example)
        return self
    
    def format(self, **kwargs) -> str:
        """Format the prompt with variables"""
        return str(self).format(**kwargs)