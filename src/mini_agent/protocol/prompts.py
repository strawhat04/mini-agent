from mini_agent.domain.tools import ToolSpec
import json
from dataclasses import asdict

def build_system_prompt(tools: list[ToolSpec]) -> str :
    """Assign behaviour and specify tool specs"""
    behavior = 'you are an assistant that replies with exactly one JSON object and nothing else. Below all available tool information;'
    tool_spec = {}
    for tool in tools:
        schema = tool.input_schema
        tool_spec[tool.name] = {
            "description" : tool.description,
            "schema" : asdict(schema)
        }

    return json.dumps({'persona' : behavior, 'tool_spec' : tool_spec})