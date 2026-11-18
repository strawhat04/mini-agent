import asyncio
from httpx import AsyncClient, Timeout

from mini_agent.agent.agent import MiniAgent

from mini_agent.llm.ollama import OllamaLLM
from mini_agent.settings import Settings
from mini_agent.domain.messages import Message
from mini_agent.protocol.prompts import build_system_prompt
from mini_agent.tools.calculator import calculator
from mini_agent.domain.policy import Policy


GOOD_MSG = [
    Message(role="system", content=build_system_prompt([calculator.spec])),
    Message(role='user', content="What is 17 multiplied by 23?")
]

BAD_MSG =[
    Message(role='user', content="YO WASSUP")
]

registry = {
    'calculator' : calculator
}
policy = Policy(allowed_tools=frozenset(['calculator', 'web_search']))

async def main():
    async with AsyncClient(timeout=Timeout(200)) as client:
        ollama = OllamaLLM(
            client= client,
            settings = Settings()
        )

        agent = MiniAgent(
            llm=ollama,
            registry= registry,
            policy=policy,
            max_iterations=20
        )

        result = await agent.run_agent("what 12 multiply 29")

        print('result ', result)
asyncio.run(main())
