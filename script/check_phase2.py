from mini_agent.settings import Settings
import os
from mini_agent.errors import summarize_validation_error
from pydantic import ValidationError

default = Settings()
print(f'Default settings : {default}')

os.environ['ollama_temperature']='0.3'

default_os = Settings()
print(f'changed temp : {default_os.ollama_temperature}')

try:
    os.environ['OLLAMA_TIMEOUT_SECONDS']='0'
    os.environ['OLLAMA_NUM_PREDICT']='-5'
    os.environ['OLLAMA_TEMPERATURE']='9'
    os.environ['OLLAMA_BASE_URL']='non-url'
    os.environ['API_PORT']='abc'
    default_fail = Settings()
except ValidationError as exc:
    result = summarize_validation_error(exc)
    print(f'validation failed {result}')


