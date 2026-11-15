from pydantic import BaseModel, Field, ConfigDict, StringConstraints, TypeAdapter
from typing import Literal, Any, Annotated


class ToolCallDecision(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    type : Literal['tool_call']
    name : str = Field(min_length=1, max_length=64, pattern='^[a-z_][a-z0-9_]*$')
    arguments : dict[str, Any]

class FinalDecision(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    type : Literal['final']
    content : Annotated[str , StringConstraints(strip_whitespace=True,min_length=1, max_length=4000)]

Decision = Annotated[ToolCallDecision | FinalDecision, Field(discriminator='type')]
_decision_adapter = TypeAdapter(Decision)