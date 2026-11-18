from mini_agent.domain.tools import ToolCall, ToolResult, ToolSuccess

def render_tool_result(call: ToolCall, result : ToolResult) -> str:
    name = call.name
    
    if isinstance(result, ToolSuccess):
        status = "ok"
        tool_result = result.result
        return f'{name} status={status} result = {tool_result}'
    else:
        reason = result.error_message
        return render_rejected_call(call, reason)
    

def render_rejected_call(call: ToolCall, reason: str) -> str :
    name = call.name
    status = "error"
    return f'{name} status={status} result = {reason[:500]}'