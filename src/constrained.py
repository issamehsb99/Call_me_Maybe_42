import numpy as np 
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()


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


def get_brakcets(self, state : str, tokens: list[int]):
    tokens_cpy = tokens.copy()
    if state == "start":
        tokens_cpy += self.encode("[{").tolist()[0]
    elif state == "mid":
        tokens_cpy += self.encode("},{").tolist()[0]
    if state == "end":
        tokens_cpy += self.encode("}]").tolist()[0]
    return tokens_cpy

def get_word(self, word: str, tokens):
    tokens_cpy = tokens.copy()
    ids = self.encode(word).tolist()[0]

    tokens_cpy += ids
    return tokens_cpy


def get_parametre(self, typ: str, token: list):
    token_cpy = token.copy()
    if typ == "number":
        id_number = self.encode("0123456789,").tolist()[0]
        token_cpy += id_number
    elif typ == "bool":
        id_bool = self.encode("True false")
        token_cpy += id_bool
    return token_cpy

