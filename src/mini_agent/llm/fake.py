from dataclasses import dataclass
from typing import Any

@dataclass
class FakeLLM:
    response : list[Any]
    current_index : int = 0
    
    def generate(self, context : list[Any]):

        if self.current_index > len(self.response):
            raise RuntimeError("Fake LLM has no more scripted response")

        result = self.response[self.current_index]
        self.current_index += 1

        return result

    
