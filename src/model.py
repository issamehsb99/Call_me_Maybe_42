from .llm_sdk import Small_LLM_Model
import numpy as np 
from .constrained import constrained_function_name , get_brakcets ,get_word
from .utils import  get_user_prompt , get_my_prompt , get_fun_id, encode_fun
import json
import datetime, time




# model = Small_LLM_Model()

def get_name_pa(self,para: dict) -> list[int]:
    li = []
    for i in para.keys():
        l = self.model.encode(f'"{i}":').tolist()[0]
        # print(model.decode(l)[0]
        li.append(l)

    return li
def get_type(para):
    li_type = []
    for i in para.values():
        li_type.append(i["type"])
    return(li_type)

def get_fun_parametre(fun_name:str):
    path = "data/input/functions_definition.json"
    with open(path, "r") as f:
        data = json.load(f)
    fun_para = {}
    for i in data:
        fun_para[i["name"]] = i["parameters"]
    para = fun_para[fun_name]
    return para

def get_full_number(self, tokens, resulta):
    targets = "-0123456789."
    stoped = ['"', ","]
    tar_stop = [self.model.encode(c) for c in stoped]
    targets_ids = []
    for i in targets:
        targets_ids += self.model.encode(i).tolist()[0]
    targets_ids += tar_stop
    while (True):
        logits = self.model.get_logits_from_input_ids(tokens)
        filtred = np.full_like(logits, -np.inf)
        for i in targets_ids:
            filtred[i] = logits[i]
        next_token = int(np.argmax(filtred))
        if next_token == self.model.encode("\"").tolist()[0][0]:
            break
        if next_token != self.model.encode(","):
            tokens.append(next_token)
            resulta.append(next_token)
        if next_token in tar_stop:
            break

def get_full_str(self, tokens, resulta):
    while True:
        logits = self.model.get_logits_from_input_ids(tokens)
        next_token = int(np.argmax(logits))
        token = self.model.decode(next_token)
        if '"' in token :
            splited = token.split('"')[0]
            if not splited:
                break
            ids = self.model.encode(splited).tolist()[0]
            tokens.extend(ids)
            resulta.extend(ids)
            break
        resulta.append(next_token)
        tokens.append(next_token)
     
def get_name_and_type(self ,resulta,tokens, num_para, para):
    i = 0
    for k, v in para.items():
        if i < num_para and i > 0:
            resulta += self.model.encode(",").tolist()[0]
            tokens += self.model.encode(",").tolist()[0] 
        tokens += get_name_pa(self,para)[i]
        resulta += get_name_pa(self,para)[i]
        if v["type"] == "number":
            get_full_number(self, tokens, resulta)
        if v["type"] == "string":
            id = self.model.encode('"').tolist()[0][0]
            tokens.append(id)
            resulta.append(id)
            get_full_str(self, tokens, resulta)
            tokens.append(id)
            resulta.append(id)
        i += 1

class Model:
    model: Small_LLM_Model = Small_LLM_Model()
    fn_de:list[dict]
    li_prompts : list = get_user_prompt()
    user_prompt: str = "" 
    fn_name:str = ""
    start = 1;
    def process(self,tokens, prompt):
        fun_name_li :list = get_fun_id(self)
        resulta = []
        if self.start:
            resulta = get_brakcets(self, "start", resulta)
            tokens = get_brakcets(self ,"start", tokens)
        else:
            resulta = get_brakcets(self, "mid", resulta)
            tokens = get_brakcets(self ,"mid", tokens)
        resulta = get_word(self, f"\"prompt\":\"{self.user_prompt}\",", resulta) 
        tokens = get_word(self, f"\"prompt\":\"{self.user_prompt}\",", tokens)
        tokens = get_word(self, "\"name\":", tokens)
        resulta = get_word(self, "\"name\":", resulta)
        tokens += self.model.encode("\"").tolist()[0]
        resulta += self.model.encode("\"").tolist()[0]
        fn_name_ids = constrained_function_name(self,fun_name_li, tokens)
        self.fn_name = self.model.decode(fn_name_ids)
        resulta += fn_name_ids
        resulta += self.model.encode("\"")[0].tolist()
        tokens += self.model.encode("\"")[0].tolist()
        tokens = get_word(self, ",\"parameters\":{", tokens)
        resulta = get_word(self, ",\"parameters\":{", resulta)
        para = get_fun_parametre(self.fn_name)
        num_para = len(para.keys())
        get_name_and_type(self, resulta ,tokens, num_para, para)
        # print("\n\n\n =====", self.model.decode(tokens))
        return tokens, resulta
    
    def main(self):
        result: list[int] = []
        result = get_my_prompt(self)
        r_final = []
        for prompt in self.li_prompts:
            self.user_prompt = prompt
            result ,j = self.process(result, prompt)
            # print(self.model.decode(j))
            r_final += j# result = output
            self.start = 0
        r_final = get_brakcets(self ,"end", r_final)
        return self.model.decode(r_final)
mod = Model()
begin_time= time.perf_counter()
resulta = mod.main()
# with open("oj.json", 'w+')as f:
#     json.dump(json.loads(resulta), f, indent=4)
print(resulta)
end_time = time.perf_counter()
print("\ntime ==========" , datetime.timedelta( end_time - begin_time ))
print((end_time - begin_time)/60)
