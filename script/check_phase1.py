from mini_agent.tools.calculator import calculator
from mini_agent.runtime.runtime import Runtime
from mini_agent.domain.tools import ToolCall

call_normal = ToolCall(name='calculator', args={'a': 1, 'b' : 2, 'expr' : 'add'})
runtime = Runtime(call=call_normal, tool=calculator)

runtime.execute_tool()