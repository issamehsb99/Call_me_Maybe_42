import json
from pydantic import BaseModel, ValidationError


class FunctionCalling(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]


def functions() -> list:
    from .model import parse_args
    arg = parse_args()
    path = arg.functions_definition
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except IOError as e:
        print("error : ", e)
    funcs = []
    for dt in data:
        try:
            fn = FunctionCalling.model_validate(dt)
            funcs.append(fn)
        except ValidationError as e:
            print("Validation error:")
            print(e)
    return funcs
