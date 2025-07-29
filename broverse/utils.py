from datetime import datetime, timezone
import yaml

def get_timestamp():
    dt = datetime.now(timezone.utc)
    return dt.isoformat()

def load_prompt_template(yaml_path):
    """Load YAML prompt config and convert to formatted string template"""
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    
    prompt = f"{config['persona']}\n\n"
    prompt += "Your job is to:\n"
    for instruction in config['instructions']:
        prompt += f"- {instruction}\n"
    prompt += f"\nTOOLS:\n{config['tools_placeholder']}\n\n"
    prompt += f"Return only the tool name, nothing else, in {config['structured_output']['format']}:\n"
    prompt += config['structured_output']['schema'] + "\n\n"
    prompt += "Examples:\n"
    for example in config['examples']:
        prompt += f"USER_INPUT: \"{example['user_input']}\"\nOUTPUT:\n{example['output']}\n"
    
    return prompt

# Usage
# tool_selector_prompt = load_prompt_template('prompts/tool_selector.yaml')
# Then use: tool_selector_prompt.format(tools=your_tools)
