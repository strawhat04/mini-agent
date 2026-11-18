import json
from dataclasses import asdict

from mini_agent.llm.ollama import OllamaLLM
from mini_agent.domain.tools import  ToolCall, ToolFailure, RegisteredTool
from mini_agent.domain.policy import Policy
from mini_agent.runtime.runtime import Runtime
from mini_agent.domain.messages import  Message
from mini_agent.protocol.prompts import build_system_prompt

from mini_agent.agent.observation import render_rejected_call, render_tool_result
from mini_agent.domain.results import AgentResult, TerminationReason
from mini_agent.errors import ModelProtocolError

class MiniAgent:
    def __init__(self, llm: OllamaLLM, registry: dict[str, RegisteredTool], policy: Policy, max_iterations: int) -> None:
        self.llm = llm
        self.registry = registry
        self.policy = policy
        self.max_iterations = max_iterations

    async def run_agent(self, user_message: str):

        tool_specs = [tool.spec for tool in self.registry.values()]
        messages = [
            Message('system', content=build_system_prompt(tool_specs)),
            Message('user', user_message)
        ]

        seen : set[tuple[str,str]] = set()
        tool_failures=0
        tool_calls_cnt = 0 

        for i in range(self.max_iterations):
            try:
                decision = await self.llm.generate(messages=messages)
            except ModelProtocolError:
                return AgentResult(
                    termination=TerminationReason.model_protocol_error,
                    answer=None,
                    model_calls=i+1,
                    tool_calls=tool_calls_cnt,
                    tool_failures=tool_failures
                )

            if isinstance(decision, ToolCall):

                tool = decision 
                tool_called = tool.name
                args_called = json.dumps(tool.args, sort_keys=True)
                messages.append(
                    Message('assistant', json.dumps({"type": "tool_call", "name": tool_called, "arguments": tool.args}))
                )
                if any(tool==tool_called and args_calls==args_called for tool, args_calls in seen) :
                    return AgentResult(
                        termination=TerminationReason.repeated_tool_call,
                        answer=None,
                        model_calls=i+1,
                        tool_calls=tool_calls_cnt,
                        tool_failures=tool_failures
                    )

                seen.add((tool_called, args_called))

                if tool.name not in self.registry:
                    observation = render_rejected_call(tool, "unknown tool")

                elif not self.policy.is_allowed(tool.name):
                    observation = render_rejected_call(tool, "tool not allowed")

                else:
                    tool_result = Runtime(tool, self.registry[tool.name]).execute_tool()
                    tool_calls_cnt += 1
                    if isinstance(tool_result, ToolFailure):
                        tool_failures+=1
                    observation = render_tool_result(tool, tool_result)

                messages.append(
                    Message('tool', observation)
                )

            else:
                return AgentResult(
                    termination= TerminationReason.final_answer,
                    answer=decision.response,
                    model_calls=i+1,
                    tool_calls=tool_calls_cnt,
                    tool_failures=tool_failures
                )

        return AgentResult(
                termination=TerminationReason.max_iteration,
                answer=None,
                model_calls=self.max_iterations,
                tool_calls=tool_calls_cnt,
                tool_failures=tool_failures         
            )        


