from dataclasses import dataclass
from mini_agent.domain.tools import ToolCall, ToolFailure, ToolSuccess, ToolResult, RegisteredTool
from mini_agent.errors import summarize_validation_error, ToolNameMismatch
from pydantic import ValidationError, BaseModel

@dataclass
class Runtime:
    call : ToolCall
    tool : RegisteredTool

    def _validator_request(self) -> BaseModel:

        # check tool name
        if self.call.name != self.tool.spec.name:
            raise ToolNameMismatch('Invalid Request : Incorrect tool name passed')

        return self.tool.args_model.model_validate(self.call.args)

    def execute_tool(self) -> ToolResult:
        """Validate args & Execute Tool """

        try:
            validated = self._validator_request()
        except ToolNameMismatch:
            return ToolFailure(
                tool_name=self.tool.spec.name,
                error_message="Invalid request: incorrect tool name passed")
        except ValidationError as e:
            return ToolFailure(
                tool_name=self.tool.spec.name,
                error_message=f"Invalid request: {summarize_validation_error(e)}",
            )
        
        try:
            result = self.tool.implementation(**validated.model_dump())
            return ToolSuccess(tool_name=self.tool.spec.name, result=result)
        except ZeroDivisionError:
            return ToolFailure(
                tool_name=self.tool.spec.name,
                error_message='Execution error: division by zero',
            )

