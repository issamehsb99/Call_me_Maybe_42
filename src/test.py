prompt1 = """ You are a function-calling assistant.
Your task is to read the user request and choose the correct function to call.
You must answer ONLY with valid JSON.
Do not explain.
Do not add markdown.
Do not write text before or after the JSON.
Available functions:"""

import json

# path = "/kaggle/input/datasets/issamhasbi/input-data/function_calling_tests.json"


prompt1 = """ You are a function-calling assistant.
Your task is to read the user request and choose the correct function to call.
You must answer ONLY with valid JSON.
Do not explain.
Do not add markdown.
Do not write text before or after the JSON.
Available functions:"""
p1_ids= model.encode(prompt1)
import json

# path = "/kaggle/input/datasets/issamhasbi/input-data/function_calling_tests.json"

import json
from pydantic import BaseModel, ValidationError


class TypeInfo(BaseModel):
    type: str


class FunctionCalling(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

def functions() -> list:
    path = "/kaggle/input/datasets/issamhasbi/input-data/functions_definition.json"

    with open(path, "r") as f:
        data = json.load(f)

    funcs = []

    for dt in data:
        try:
            fn = FunctionCalling.model_validate(dt)
            funcs.append(fn)
        except ValidationError as e:
            print("Validation error:")
            print(e)

    return funcs

    prompt1 = """ You are a function-calling assistant.
Your task is to read the user request and choose the correct function to call.
You must answer ONLY with valid JSON.
Do not explain.
Do not add markdown.
Do not write text before or after the JSON.
Available functions:"""


import math

p = "solve this equation : "
inputs_ids1 = model.encode(p)[0].tolist()
input_ids = model.encode(prompt)[0].tolist()
target = "0123456789-+.'"
logits1= model.get_logits_from_input_ids(inputs_ids1)
for _ in range(25):
    logits = model.get_logits_from_input_ids(input_ids)
    logits = logits1 + logits
    mask = [-math.inf] * len(logits)
    for e in target:
        e_id = model.encode(e)[0].tolist()[0]
        mask[e_id] = logits[e_id]
    last_token_logits = mask.index(max(mask))
    if model.decode(last_token_logits) in ".',":
        break
    print(model.decode(last_token_logits))
    input_ids.append(last_token_logits)
model.decode(input_ids)
fn = functions()
add = ""
l = 1 
for i in fn:
    fct =f"name :{i.name} his description: {i.description} his arguments {i.parameters} and she return {i.returns}"
    add = add + f"function {l} " + fct + "\n"
    l =+1
print(add)


# model = Small_LLM_Model()

# class model_use(BaseModel):
#     def constrained_function_name()
