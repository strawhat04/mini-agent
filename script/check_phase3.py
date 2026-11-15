from mini_agent.runtime.runtime import Runtime
from mini_agent.tools.registry import build_registry
from mini_agent.domain.tools import ToolCall

cases = [
    {"a": 17, "b": 23, "expr": "multiply"},
    {"a": 1, "b": 0, "expr": "divide"},
    {"a": "17", "b": 23, "expr": "multiply"},
    {"a": True, "b": 2, "expr": "add"},
    {"a": 1, "b": 2},
    {"a": 1, "b": 2, "expr": "pow"},
    {"a": 1, "b": 2, "expr": "add", "c": 9},
    {"a": float("nan"), "b": 1, "expr": "add"}
]

get_tools = build_registry()
calculator = get_tools.get('calculator')

if not calculator:
    raise ValueError

for idx, arg in enumerate(cases):
    call = ToolCall(name='calculator', args=arg)
    tool = calculator 
    run = Runtime(call, tool)
    result = run.execute_tool()
    print(f"case - {idx} : Result : {result}")




