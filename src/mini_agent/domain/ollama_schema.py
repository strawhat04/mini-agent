from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import Any
from mini_agent.domain.messages import Message

class OllamaMessage(BaseModel):
    role : str
    content : str
    thinking : str | None = None

class OllamaChatResponse(BaseModel):
    message : OllamaMessage
    done : bool
    done_reason : str | None = None
    eval_count : int | None = None


@dataclass
class PayloadOptions:
    num_predict : int = 256
    temperature : float = 0.2 

@dataclass
class Payload:
    model : str 
    messages : list[Message]
    format : dict[str, Any]
    options : PayloadOptions = field(default_factory=PayloadOptions)
    stream : bool = False
    think : bool = False
