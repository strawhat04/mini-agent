from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import AnyHttpUrl, Field, TypeAdapter

class Settings(BaseSettings):
    "Class to configure environment settings"
    model_config = SettingsConfigDict(extra='ignore')

    ollama_base_url : AnyHttpUrl = TypeAdapter(AnyHttpUrl).validate_python('http://localhost:11434')
    ollama_model : str = Field(default="qwen3:4b", min_length=1)
    ollama_timeout_seconds : float = Field(default=60, gt=0, le=600, allow_inf_nan=False)
    ollama_num_predict : int = Field(default=256, ge=1, le=4096)
    ollama_temperature : float = Field(default=0.5, ge=0, le=2,allow_inf_nan=False)
    agent_max_iterations : int = Field(default=5, ge=1, le=20)
    max_concurrent_runs : int = Field(default=1, ge=1, le=8)
    queue_wait_seconds : float = Field(default=5, gt=0, allow_inf_nan=False)
    request_timeout_seconds : float = Field(default=90, gt=0, allow_inf_nan=False)
    api_host : str = "127.0.0.1"
    api_port : int = Field(default=8000, ge=1, le=65535)
