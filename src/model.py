from .llm_sdk import Small_LLM_Model
import numpy as np
import json
from constrained import get_brakcets, get_parametre, get_word ,constrained_function_name
# from load_fun import functions
from utils import get_user_prompt, get_fun_id ,get_my_prompt
from pydantic import BaseModel, ValidationError


class Model:
    model: Small_LLM_Model = Small_LLM_Model()
    fn_de:list[dict]
    my_prompt_id = get_my_prompt(model)
    fun_name_li :list = get_fun_id()
    li_prompts : list = get_user_prompt()
    user_prompt: str = "" 
    fn_name:str = ""
    def process(self,tokens):
        tokens = get_brakcets(self ,"start", tokens)
        tokens = get_word(self, f"\"prompt\"\"{self.user_prompt}\",", tokens)
        tokens = get_word(self, "\"name\":", tokens)
        return tokens
    def main(self):
        result: list[int] = []
        for prompt in self.li_prompts:
            result = []
            self.user_prompt = prompt
            output = self.process(result)
            prompt_id = self.model.encode(prompt).tolist()[0]
            ids = self.my_prompt_id + prompt_id
            output += constrained_function_name(self.fun_name_li, ids)
            print(self.model.decode(output))

# def main:
#     model = Model(model=Small_LLM_Model(),
#                   fn_def=data
#                   )












# i = 1
# function_ids = [[8522, 265, 322], [8522, 4555, 456], [8522, 5566, 4111], [85111, 455 , 65655]]
# { 4111}
# gen_ids = [8522, 5566]
# [for ids in functions_ids if gen_ids == ids[:i]]
# i = 2
# [[: i]]


for prompt in li_prompt:
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


