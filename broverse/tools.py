import inspect
import typing
from typing import get_type_hints

def python_type_to_json_type(py_type):
    origin = typing.get_origin(py_type) or py_type

    if origin in [int]:
        return "integer"
    elif origin in [float]:
        return "number"
    elif origin in [bool]:
        return "boolean"
    elif origin in [str]:
        return "string"
    elif origin in [list, tuple]:
        return "array"
    elif origin in [dict]:
        return "object"
    else:
        return "string"  # fallback

def convert_to_tool(func) -> dict:
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    parameters = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for name, param in sig.parameters.items():
        param_type = type_hints.get(name, str)
        param_schema = {"type": python_type_to_json_type(param_type)}
        parameters["properties"][name] = param_schema
        if param.default is param.empty:
            parameters["required"].append(name)

    tool = {
        "name": func.__name__,
        "description": func.__doc__ or "",
        "parameters": parameters
    }

    return tool

def register_tools(tools:list):
    _tools = {}
    for tool in tools:
        tool_definition = convert_to_tool(tool)
        name = tool_definition.get("name", None)
        _tools[name] = {
            "definition": tool_definition,
            "tool": tool
        }
    return _tools