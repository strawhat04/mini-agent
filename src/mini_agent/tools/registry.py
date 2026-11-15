from mini_agent.domain.tools import RegisteredTool
from mini_agent.tools.calculator import calculator

def build_registry() -> dict[str, RegisteredTool]:
    return {'calculator' : calculator}
