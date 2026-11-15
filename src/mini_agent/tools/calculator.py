from typing import Literal
from mini_agent.domain.tools import ToolSpec, RegisteredTool

def calculate(a: float, b: float, expr : Literal['add', 'sub', 'multiply', 'divide']) -> float:
    if not isinstance(a, (int, float)) :
        raise TypeError(f"Expect arg a to be numeric but received {type(a)}")
    if not isinstance(b, (int, float)) :
            raise TypeError(f"Expect arg b to be numeric but received {type(a)}")
    
    if expr =='add':
        return a + b
    elif expr == 'sub':
        return a - b 
    elif expr == 'multiply':
        return a * b
    elif expr == 'divide':
        return float(a/b)
    else:
        raise TypeError(f"Invalidate expr type : expected ['add', 'sub', 'multiply', 'divide'] but received {expr}")


calculator_spec = ToolSpec(
    name='calculator',
    description='compute mathematical expression between variables',
    input_schema= {
        'a' : (int,float),
        'b' : (int, float),
        'expr' : Literal['add', 'sub', 'multiply', 'divide']
    },
)

calculator = RegisteredTool(
     spec=calculator_spec,
     implementation=calculate
)