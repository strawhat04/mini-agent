from dataclasses import dataclass

@dataclass(frozen=True)
class Policy:
    allowed_tools : frozenset[str]

    def is_allowed(self, tool_name:str) -> bool:
        return tool_name in self.allowed_tools
