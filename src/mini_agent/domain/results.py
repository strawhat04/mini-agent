from dataclasses import dataclass
from enum import StrEnum


class TerminationReason(StrEnum):
    final_answer = "final_answer"
    max_iteration = "max_iteration"
    repeated_tool_call = "repeated_tool_call"
    model_protocol_error = "model_protocol_error"


@dataclass(frozen=True)
class AgentResult:
    termination : TerminationReason
    answer : str | None
    model_calls : int
    tool_calls : int
    tool_failures : int

    def __post_init__(self):

        if self.termination == TerminationReason.final_answer and self.answer is None:
            raise ValueError('Answer could not be None if termination reason is final answer') 

    @property
    def succeeded(self):
        return self.termination==TerminationReason.final_answer
    