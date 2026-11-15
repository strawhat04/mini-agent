from dataclasses import dataclass, asdict
from pydantic import ValidationError
from loguru import logger

from httpx import AsyncClient, ConnectError, TimeoutException, HTTPStatusError, HTTPError 
from typing import Any

from mini_agent.protocol.decision import parse_decision
from mini_agent.domain.tools import ToolCall
from mini_agent.domain.messages import FinalResponse 
from mini_agent.settings import Settings
from mini_agent.domain.ollama_schema import Payload, PayloadOptions, PayloadMessage, OllamaChatResponse, OllamaMessage
from mini_agent.errors import ModelUnavailableError, ModelTimeoutError,ModelResponseError, ModelProtocolError
from mini_agent.protocol.decision import decision_json_schema

@dataclass
class OllamaLLM:
    client : AsyncClient
    settings : Settings

    async def generate(self, messages : list[PayloadMessage]) -> ToolCall | FinalResponse:

        payload = self._build_payload(model=self.settings.ollama_model, messages=messages)
        logger.debug(f'Received payload : {payload}')

        url = f'{str(self.settings.ollama_base_url).rstrip('/')}/api/chat'
        logger.debug(f'URL OLLAMA : {url}')
        try:
            response = await self.client.post(
                url = url,
                json = payload
            )
            status_code = response.status_code
            logger.debug(f'Request Status : {status_code}')
            logger.debug(f'Content of response : {response.content}')

            response.raise_for_status()
            json_result = response.json()
        except ConnectError as exc:
            raise ModelUnavailableError(exc) from exc
        except TimeoutException as exc:
            raise ModelTimeoutError(exc) from exc
        except HTTPStatusError as exc:
            status_group= str(status_code)[0]
            if status_group == '4':
                raise ModelResponseError(exc) from exc
            if status_group == '5':
                raise ModelUnavailableError(exc) from exc
            if status_group == '3':
                raise ModelUnavailableError(exc)  from exc
        except ValueError as exc:
            raise ModelResponseError("LLM response is not in JSON format, validate request")  from exc

        ollama_response = self._convert_chat_response(json_result)

        self._validate_ollama_response(ollama_response)

        return parse_decision(ollama_response.message.content)
     

    async def is_ready(self) -> bool :

        try:
            url =  f'{str(self.settings.ollama_base_url).rstrip('/')}/api/tags'
            response = await self.client.get(url)

            status_code = response.status_code
            response.raise_for_status()
            content = response.json()
        except HTTPError:
            return False
        except ValidationError:
            return False
        
        models = content.get('models',[])
        contain_model = any(m.get("name") == self.settings.ollama_model for m in models)
        return status_code==200 and contain_model
    
    def _build_payload(self, model : str, messages : list[PayloadMessage])  -> dict[str, Any] :

        payload_options = PayloadOptions(
            num_predict=self.settings.ollama_num_predict,
            temperature=self.settings.ollama_temperature
        )
        payload = Payload(
            model=model,
            messages= messages,
            format= decision_json_schema(),
            options=payload_options
        )

        return asdict(payload)

    def _convert_chat_response(self, json_output: dict[str, Any]) -> OllamaChatResponse:

        try:
            validate_response = OllamaChatResponse.model_validate(json_output)
            return OllamaChatResponse(**validate_response.model_dump())
        except ValidationError as exc:
            raise ModelResponseError(exc) from exc

    def _validate_ollama_response(self, response : OllamaChatResponse) -> None:

        if response.done_reason == 'length':
            raise ModelProtocolError('output was cut off; never parse it')
        if not response.message.content:
            raise ModelResponseError('Returned empty content')

