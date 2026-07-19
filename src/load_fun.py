import json
from pydantic import BaseModel, ValidationError


class FunctionCalling(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

def functions() -> list:
    path = "data/input/functions_definition.json"

    with open(path, "r") as f:
        data = json.load(f)
   
    funcs = []
    fun_par={}
    for dt in data: 
        
        try:
            fn = FunctionCalling.model_validate(dt)
            funcs.append(fn)
        except ValidationError as e:
            print("Validation error:")
            print(e)
    return funcs


