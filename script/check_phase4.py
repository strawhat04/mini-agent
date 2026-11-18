from mini_agent.protocol.decision import parse_decision
from mini_agent.protocol.prompts import build_system_prompt
from mini_agent.tools.calculator import calculator
from mini_agent.errors import ModelProtocolError

#test parse_decision
test_cases = [
    '{"type": "tool_call", "name": "calculator", "arguments": {"a": 17, "b": 23}}',
    '{"type": "final", "content": "Done"}',
    "not json",
    "",
    "[]",
    '{"type": "dance"}',
    '{"type": "tool_call", "name": "calculator"}',
    '{"type": "tool_call", "name": "calculator", "arguments": "17*23"}',
    '{"type": "final", "content": " "}',
    '{"type": "final", "content": "hi", "extra": 1}',
    '{"type": "tool_call", "name": "__import__(\'os\')", "arguments": {}}',
    "a" * 20000,
]

for idx, case in enumerate(test_cases):
    try:
        result = parse_decision(case)
        print(f'Passed case {idx} : result = {result}')
    except ModelProtocolError as e :
        print(f'Failed case {idx} : result = {e}')
    

#test check system_prompt
print(f'Test Prompt :\n Result : {build_system_prompt([calculator.spec])}')