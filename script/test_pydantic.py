from pydantic import BaseModel, ValidationError

class arguments(BaseModel):
    num : int
    msg : str

if __name__=='__main__':
    from mini_agent.errors import summarize_validation_error
    try:
        arg = arguments(num='/xx', msg='check')
    except ValidationError as e:
        print("here I'm", e.errors())
        print("check results : -", summarize_validation_error(e))
