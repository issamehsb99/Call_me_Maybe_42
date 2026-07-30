import json
from .load_fun import functions


def get_fun(self):
    fn = functions()
    add = ""
    fun_name = []
    for i in fn:
        p = []
        for k, v in i.parameters.items():
            p.append(
                    f"{k}: "
                    f"{'float' if v['type'] == 'number' else v['type'][:3]}"
                )
        fct = f"{i.name}({', '.join(p)}): {i.description}"
        add += fct + "\n"
        fun_name.append(i.name)
    fun_name_id = [self.model.encode(f).tolist()[0] for f in fun_name]
    return fun_name_id, add


def get_fun_id(self) -> list[int]:
    ids, i = get_fun(self)
    i = i
    return ids


def encode_fun(self):
    id, fun = get_fun(self)
    id = id
    ids = self.model.encode(fun).tolist()[0]
    return ids


def get_my_prompt(self, prompt):
    prompt1 = f"""
    you are a function calling system.
    you will given a user prompt and convert it to a function calling format.


    FUNCTIONS:
    {get_fun(self)[1]}

    TASK:
    user_prompt: {prompt}

    OUTPUT:
    """
    ids = self.model.encode(prompt1).tolist()[0]
    ids += encode_fun(self)
    return ids


def get_user_prompt() -> list[str]:
    from .model import parse_args
    arg = parse_args()
    try:
        with open(arg.input, 'r') as f:
            data = json.load(f)
    except IOError as e:
        print(e)
    li_prompt = []
    li_final = []
    for i in data:
        li_prompt.append(i.get("prompt"))
    for pr in li_prompt:
        if not pr:
            continue
        pr = pr.replace("\t", " ")
        pr = pr.replace("\n", " ")
        if "\\" in pr:
            pr = pr.replace("\\", "\\\\")
        if "\"" in pr:
            pr = pr.replace('\"', '\\"')
        li_final.append(pr)
    return li_final
