from pydantic import ValidationError

class ToolNameMismatch(Exception):
    """Raised when a ToolCall's name does not match the registered tool""" 

class AgentError(Exception):
    "Base Exception Class for every other custom error class"

class ModelProtocolError(AgentError):
    "Invalide Model Response such as invalid JSON, unknown tool name, fail pydantic schema"

class ModelUnavailableError(AgentError):
    "Model is not reachable, or server return 5xx"

class ModelTimeoutError(AgentError):
    "Model took too long to responsd and intentionally failed"

class ModelResponseError(AgentError):
    "Missing strucutre or malformed output"

def summarize_validation_error(exc: ValidationError) -> str:
    "Simplify validation error to pass to agent"

    err_msg = ""
    if not exc.errors():
        return 'no error'
    
    for error in exc.errors():
        loc = ".".join(str(item) for item in error.get('loc'))
        msg = error.get('msg')
        err_msg += str(loc) + ":" + msg + ";"

    return err_msg[:300]