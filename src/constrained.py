import numpy as np 
from .llm_sdk import Small_LLM_Model
import numpy as np 

# model = Small_LLM_Model()

def extract_token_n(ids, n):
    """that function extract token n from ids """
    chose = set()
    for i in ids:
        if len(i) > n:
            chose.add(i[n])
    return(chose)

def constrained_function_name(self,fun_name_li: list , input_id:list):
    just_copy = fun_name_li.copy()
    # print("===" , model.decode(fun_name_li))
    n = 0
    output = []
    while(True):
        logits = self.model.get_logits_from_input_ids(input_id)
        chosen = extract_token_n(just_copy, n)
        if not chosen:
            break
        filtred = np.full_like(logits, -np.inf)

        for t in chosen:
            filtred[t] = logits[t]
        next_token = int(np.argmax(filtred))
        input_id.append(next_token)
        
        output.append(next_token)
        chosen.remove(next_token)
        # print("output ====", model.decode(output))
        if (self.model.decode(np.argmax(logits)) == "\""):
            break
        just_copy = [
            l for l in just_copy
            if len(l) > n and l[n] == next_token
                    ]
        if any(n == len(l) for l in just_copy):
            break
        n +=1
    # print(output)
    return output


def get_brakcets(self, state : str, tokens: list[int]):
    tokens_cpy = tokens.copy()
    if state == "start":
        tokens_cpy += self.model.encode("[{").tolist()[0]
    elif state == "mid":
        tokens_cpy += self.model.encode("}},{").tolist()[0]
    if state == "end":
        tokens_cpy += self.model.encode("}}]").tolist()[0]
    return tokens_cpy

def get_word(self, word: str, tokens):
    tokens_cpy = tokens.copy()
    ids = self.model.encode(word).tolist()[0]

    tokens_cpy += ids
    return tokens_cpy


def get_parametre_from_t(self, typ: str):
    
    target_bool = ["ture", "false"]
    # numbers : int str bool 
    # target_nbr = ["""1"23456789,-+"]
    print(typ  ,"\n")
    if typ == "number":
        id_number = self.model.encode(".0123456789-").tolist()[0]
        token_cpy = id_number
        return token_cpy
    elif typ == "int" :
        arr = ['.', ',', '-', '+'] + [str(x) for x in range(10)]
        id_number = []
        for e in arr:
            id_token = self.model.encode(e)[0].tolist()[0]
            id_number.append(id_token)
        # id_number = model.encode("-0123456789").tolist()[0] + model.encode(".").tolist()[0] + model.encode(",").tolist()[0]
        token_cpy = id_number
        return token_cpy
    elif typ == "bool":
        id_bool = self.model.encode("True false")
        token_cpy = id_bool
        return token_cpy


# for token_id in id_number:
#     print(model.decode(token_id))
