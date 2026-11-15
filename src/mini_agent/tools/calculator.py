from typing import Literal
from mini_agent.domain.tools import ToolSpec, RegisteredTool, InputSchema
from pydantic import BaseModel, Field, ConfigDict

class CalculatorArgs(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')

    a: float = Field(allow_inf_nan=False)
    b: float = Field(allow_inf_nan=False)
    expr : Literal['add', 'sub', 'multiply', 'divide']

    @classmethod
    def input_schema(cls) -> InputSchema :
        json_output = cls.model_json_schema()
        args_properties = json_output.get('properties')
        args_required = json_output.get('required')

        if not args_required or not args_properties:
            raise KeyError("Pydantic Validation JSON Schema doesn't expose required attributes")

        return InputSchema(
            args_properties=args_properties,
            args_required=args_required
        )


def calculate(a: float, b: float, expr : Literal['add', 'sub', 'multiply', 'divide']) -> float:

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
    input_schema=CalculatorArgs.input_schema()
)

calculator = RegisteredTool(
    spec=calculator_spec,
    args_model = CalculatorArgs,
    implementation=calculate
)