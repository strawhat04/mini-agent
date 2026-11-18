import asyncio
from httpx import AsyncClient, Timeout

from mini_agent.llm.ollama import OllamaLLM
from mini_agent.settings import Settings
from mini_agent.domain.messages import Message
from mini_agent.protocol.prompts import build_system_prompt
from mini_agent.tools.calculator import calculator

GOOD_MSG = [
    Message(role="system", content=build_system_prompt([calculator.spec])),
    Message(role='user', content="What is 17 multiplied by 23?")
]

BAD_MSG =[
    Message(role='user', content="YO WASSUP")
]

async def main():
    async with AsyncClient(timeout=Timeout(200)) as client:
        ollama = OllamaLLM(
            client= client,
            settings = Settings()
        )

        output_good = await ollama.generate(messages=GOOD_MSG)
        print("good_response ", output_good)

        output_bad = await ollama.generate(messages=BAD_MSG)
        print("bad_response", output_bad)

        print("is model ready", await ollama.is_ready())


asyncio.run(main())

