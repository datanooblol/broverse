import json

function_definition = { 
  "name": "add",
  "description": "Add two numbers together",
  "parameters": {
    "type": "object",
    "properties": {
      "a": { "type": "integer" },
      "b": { "type": "integer" }
    },
    "required": ["a", "b"]
  }
}

user_input = "What is the result of 1 plus 1?"

prompt = f"""\
You are a function argument extractor. 

Given the following function definition:
```json
{json.dumps(function_definition, indent=2)}
```
And the following user input:
"{user_input}"

Extract the input values required to call the function. Return a JSON object that matches the parameters schema exactly. Only include the keys that are required.

Respond only with the JSON object.
