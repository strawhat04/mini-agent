from pydantic import ValidationError
from typing import Any

from mini_agent.domain.model import _decision_adapter, ToolCallDecision, FinalDecision
from mini_agent.domain.tools import ToolCall
from mini_agent.domain.messages import FinalResponse
from mini_agent.errors import ModelProtocolError, summarize_validation_error


def parse_decision(text: str) -> ToolCall | FinalResponse:

    if len(text) > 16_000:
        raise ModelProtocolError(f'Input text exceeded | expected 16000 but received {len(text)}')

    try:
        decision = _decision_adapter.validate_json(text)
    except ValidationError as e:
        error = summarize_validation_error(e)
        raise ModelProtocolError(error) from e

    if isinstance(decision, ToolCallDecision):
        return ToolCall(
            name=decision.name,
            args=decision.arguments
        )

    elif isinstance(decision, FinalDecision):
        return FinalResponse(
            response=decision.content
        )

    else:
        raise TypeError(f'Decision Adapter expected ToolCallDecision or FinalDecision but got {type(decision).__name__}')

def decision_json_schema() -> dict[str, Any]:
    return _decision_adapter.json_schema()

def final_json_schema() -> dict[str, Any]:
    return FinalDecision.model_json_schema()