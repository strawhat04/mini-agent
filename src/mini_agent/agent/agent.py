from mini_agent.llm.fake import FakeLLM
from mini_agent.domain.tools import  ToolCall, ToolFailure
from mini_agent.runtime.runtime import Runtime
from mini_agent.domain.messages import FinalResponse
from dataclasses import dataclass
from typing import Any
from loguru import logger

@dataclass
class MiniAgent:
    response : list[Any]
    tool_registry : dict[str, Any]
    total_request : int = 20

    def __post_init__(self):
        self.llm = FakeLLM(response=self.response)

    def run_agent(self, context: list[Any]):
        self.cnt_request=0
        response = self.llm.generate(context)
        self.cnt_request += 1

        logger.info(f'Agent running {self.cnt_request} request')
        if self.cnt_request > self.total_request:
            raise RuntimeError(f'Agent requests exceed {self.total_request} requests')

        context_len = sum([len(str(chars)) for chars in context])
        logger.info(f'Agent Call {self.cnt_request} - Context length {context_len}')

        if isinstance(response, ToolCall):
            get_tool = self._get_required_tool(response.name)
            if get_tool:
                logger.debug(f'Invoking runtime with {get_tool.spec.name}')
                rt = Runtime(call=response, tool=get_tool)
                tool_result = rt.execute_tool()

                if isinstance(tool_result, ToolFailure):
                    logger.info('Updating context with tool failure details')
                    updated_context = context + [response] + [tool_result]
                else:
                    logger.info('Updating context with tool result')
                    updated_context = context + [tool_result]
                return self.run_agent(updated_context)
            else:
                updated_context = context + [response]  + [ValueError(f"{response.name} Tool does't exist in registry")]
                return self.run_agent(updated_context)
            

        if isinstance(response, FinalResponse):
            return response.response 

    def _get_required_tool(self, tool_name : str):
        return self.tool_registry.get(tool_name)