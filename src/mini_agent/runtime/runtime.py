from dataclasses import dataclass
from mini_agent.domain.tools import ToolCall, ToolFailure, ToolSuccess, ToolResult, RegisteredTool
from loguru import logger

@dataclass
class Runtime:
    call : ToolCall
    tool : RegisteredTool

    def _validator_request(self) -> None:

        # check tool name
        if self.call.name != self.tool.spec.name:
            raise ValueError(f'Incorrect tool name passed; it should be {self.tool.spec.name}')

        required_args = set(self.tool.spec.input_schema.keys())
        passed_args = set(self.call.args.keys())

        missing = required_args - passed_args
        unexpected = passed_args - required_args

        if unexpected:
            raise ValueError(f"Unexpected argument {', '.join(unexpected)}  passed into {self.tool.spec.name} tool")

        if missing:
            raise ValueError(f"Missing arguments : {self.tool.spec.name} tool requires {', '.join(missing)} argument")

        logger.success(f'{self.call.name} Tool Validation Passed')

    def execute_tool(self) -> ToolResult:
        try:
            self._validator_request()
        except ValueError as e:
            return ToolFailure(
                tool_name=self.tool.spec.name,
                error_message=f'Invalid request: {e}',
            )

        try:
            result = self.tool.implementation(**self.call.args)
            return ToolSuccess(tool_name=self.tool.spec.name, result=result)
        except ZeroDivisionError as e:
            return ToolFailure(
                tool_name=self.tool.spec.name,
                error_message=f'Execution error: {type(e).__name__}: {e}',
            )






