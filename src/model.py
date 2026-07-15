from .llm_sdk import Small_LLM_Model
import numpy as np
import json
from pydantic import BaseModel, ValidationError


model = Small_LLM_Model()
class TypeInfo(BaseModel):
    type: str


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


    for dt in data:
        try:
            fn = FunctionCalling.model_validate(dt)
            funcs.append(fn)
        except ValidationError as e:
            print("Validation error:")
            print(e)

    return funcs



def extract_token_n(ids, n):
    """that function extract token n from ids """
    chose = set()
    for i in ids:
        print("n = ", n)
        if len(i) > n:
            chose.add(i[n])
    return(chose)


def constrained_function_name(fun_name_li: list , input_id:list):
    just_copy = fun_name_li.copy()
    n = 0
    while(True):

        logits = model.get_logits_from_input_ids(input_id)
        # print("========",just_copy)
        chosen = extract_token_n(just_copy, n)
        if not chosen:
            break
        filtred = np.full_like(logits, -np.inf)

        for t in chosen:
            filtred[t] = logits[t]
        next_token = int(np.argmax(filtred))
        input_id.append(next_token)
        if (model.decode(np.argmax(logits)) == "\""):
            break
        just_copy = [
            l for l in just_copy
            if len(l) > n and l[n] == next_token
                    ]
        if any(n == len(l) for l in just_copy):
            break
        
        n +=1 



with open("data/input/function_calling_tests.json", 'r') as f:
    data = json.load(f)
prompt2=""
li_prompt = []
li_complet_pt = []

for i in data:
    li_prompt.append(i.get("prompt"))


prompt_id = ids.tolist()[0]

# i = 1
# function_ids = [[8522, 265, 322], [8522, 4555, 456], [8522, 5566, 4111], [85111, 455 , 65655]]
# { 4111}
# gen_ids = [8522, 5566]
# [for ids in functions_ids if gen_ids == ids[:i]]
# i = 2
# [[: i]]
for prompt in li_prompt:
    prompt += "JSON:```"
    id_prompt = model.encode(prompt)
    id_p = id_prompt[0].tolist()
    input_id = prompt_id + id_p


    generated_ids = []
    open_braces = 0
    started = False
    l = 0
    for _ in range(20):  # safety cap, higher than before

        l += 1
        print(l)
        constrained_function_name(fun_name_id , input_id)
        # constrained decoding 0123456789
    #     next_token_id = int(np.argmax(logits))
    #     input_id.append(next_token_id)
    #     generated_ids.append(next_token_id)
        

    #     token_str = model.decode([next_token_id])
    
    #     print(token_str, end="")
    #     #check end of generation
    #     # track brace balance to detect a complete JSON object
    #     for ch in token_str:
    #         if ch == "{":
    #             open_braces += 1
    #             started = True
    #         elif ch == "}":
    #             open_braces -= 1

    #     if started and open_braces == 0:
    #         break  # JSON object is structurally closed, stop generating

    # print("\n\n")


