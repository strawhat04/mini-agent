
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from pydantic import BaseModel

@dataclass
class ToolSpec:
    """Information about a tool that can be shown to the model."""
    name: str
    description: str
    input_schema: dict[str, Any]

@dataclass
class RegisteredTool:
    spec : ToolSpec
    implementation : Callable[..., Any]

@dataclass
class ToolCall:
    """A request from the model to execute a tool."""
    name: str
    args: dict[str, Any]

@dataclass
class ToolSuccess:
    """A successfully executed tool call."""
    tool_name: str
    result: Any


@dataclass
class ToolFailure:
    """A tool call that failed during execution."""
    tool_name: str
    error_message: str


ToolResult = ToolSuccess | ToolFailure