from llm_sdk.llm_sdk import Small_LLM_Model
import numpy as np
from .constrained import constrained_function_name, get_brakcets, get_word
from .utils import get_user_prompt, get_my_prompt, get_fun_id
import json
import argparse
from pydantic import BaseModel, Field
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed argument namespace.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Function calling tool using constrained decoding."
        )
    )

    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the functions definition JSON file.",
    )

    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the input prompts JSON file.",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calls.json",
        help="Path to the output JSON file.",
    )

    parser.add_argument(
        "--use_smol",
        action="store_true",
        help="Use SmolLM instead of default Qwen model.",
    )

    return parser.parse_args()


def get_name_pa(self: Any, para: dict) -> list[Any]:
    li = []
    for i in para.keys():
        k = self.model.encode(f'"{i}":').tolist()[0]
        li.append(k)
    return li


def get_type(para: dict[Any, Any]) -> list[str]:
    li_type = []
    for i in para.values():
        li_type.append(i["type"])
    return (li_type)


def get_fun_parametre(fun_name: str) -> Any:
    args = parse_args()
    path = args.functions_definition
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except IOError as e:
        print(e)
    fun_para = {}
    for i in data:
        fun_para[i["name"]] = i["parameters"]
    para = fun_para[fun_name]
    return para


def get_full_number(
        self: Any,
        tokens: list[Any],
        resulta: list[Any],
        ma: int) -> None:
    stoped = ['"', ","]
    targets = "-0123456789."
    num: list[int] = []
    tar_stop = [self.model.encode(c) for c in stoped]
    targets_ids = []
    for j in targets:
        targets_ids += self.model.encode(j).tolist()[0]
    targets_ids += tar_stop
    var = 0
    while (True):
        logits = self.model.get_logits_from_input_ids(tokens)
        filtred = np.full_like(logits, -np.inf)
        for i in targets_ids:
            filtred[i] = logits[i]
        next_token = int(np.argmax(filtred))
        if next_token == self.model.encode("\"").tolist()[0][0]:
            d = self.model.decode(num)
            nm = float(d)
            resulta.extend(self.model.encode(str(nm)).tolist()[0])
            break
        if next_token != self.model.encode(","):
            tokens.append(next_token)
            num.append(next_token)
        if next_token in tar_stop:
            d = self.model.decode(num)
            nm = float(d)
            resulta.extend(self.model.encode(str(nm)).tolist()[0])
            break
        if var == ma:
            d = self.model.decode(num)
            nm = float(d)
            resulta.extend(self.model.encode(str(nm)).tolist()[0])
        var += 1


def get_full_int(
        self: Any,
        tokens: list[Any],
        resulta: list[Any],
        ma: int
) -> None:
    targets = "-0123456789"
    stoped = ['"', ","]
    tar_stop = [self.model.encode(c) for c in stoped]
    targets_ids = []
    for j in targets:
        targets_ids += self.model.encode(j).tolist()[0]
    targets_ids += tar_stop
    jl = 0
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
        if jl == ma:
            break
        jl += 1


def get_full_str(
        self: Any,
        tokens: list[Any],
        resulta: list[Any]
) -> None:
    while True:
        logits = self.model.get_logits_from_input_ids(tokens)
        next_token = int(np.argmax(logits))
        token = self.model.decode(next_token)
        if "\\" in token:
            break
        if '"' in token:
            splited = token.split('"')[0]
            if not splited:
                break
            ids = self.model.encode(splited).tolist()[0]
            tokens.extend(ids)
            resulta.extend(ids)
            break
        resulta.append(next_token)
        tokens.append(next_token)


def get_bool(self: Any, tokens: list[Any], resulta: list[Any]) -> None:
    allowed = ["true", "false"]
    id_al = [self.model.encode(i) for i in allowed]
    logits = self.model.get_logits_from_input_ids(tokens)
    filtered = np.full_like(logits, -np.inf)
    for i in id_al:
        filtered[i] = logits[i]
    nex = np.argmax(filtered)
    for p in id_al:
        if nex in p:
            tokens.extend(p)
            resulta.extend(p)


def get_name_and_type(
        self: Any,
        resulta: list[Any],
        tokens: list[Any],
        num_para: int,
        para: dict,
        ma: int
) -> None:
    i = 0
    for v in para.values():
        if i < num_para and i > 0:
            resulta += self.model.encode(",").tolist()[0]
            tokens += self.model.encode(",").tolist()[0]
        for tkn in get_name_pa(self, para)[i]:
            tokens.append(tkn)
            resulta.append(tkn)
        # tokens.extend(get_name_pa(self, para)[i])
        # print(get_name_pa(self, para)[i])
        # resulta += get_name_pa(self, para)[i]
        if v["type"] == "number" or v["type"] == "float":
            get_full_number(self, tokens, resulta, ma)
        if v["type"] == "string":
            id = self.model.encode('"').tolist()[0][0]
            tokens.append(id)
            resulta.append(id)
            get_full_str(self, tokens, resulta)
            tokens.append(id)
            resulta.append(id)
        if v["type"] == "int" or v["type"] == "integer":
            get_full_int(self, tokens, resulta, ma)
        if v["type"] == "bool" or v["type"] == "boolean":
            tokens.append(id)
            resulta.append(id)
            get_bool(self, tokens, resulta)
            tokens.append(id)
            resulta.append(id)
        i += 1


class Model(BaseModel):
    model: Any = Field(default_factory=Small_LLM_Model)
    li_prompts: list = Field(default_factory=get_user_prompt)
    user_prt: str = ""
    fn_name: str = ""
    start: int = 1

    def process(self: Any, tokens: list[Any], i: int) -> Any:
        fun_name_li: list = get_fun_id(self)
        resulta: list[Any] = []
        if self.start:
            resulta = get_brakcets(self, "start", resulta)
            tokens = get_brakcets(self, "start", tokens)
        else:
            resulta = get_brakcets(self, "mid", resulta)
            tokens = get_brakcets(self, "mid", tokens)
        resulta = get_word(self, f"\"prompt\":\"{self.user_prt}\",", resulta)
        tokens = get_word(self, f"\"prompt\":\"{self.user_prt}\",", tokens)
        tokens = get_word(self, "\"name\":", tokens)
        resulta = get_word(self, "\"name\":", resulta)
        tokens += self.model.encode("\"").tolist()[0]
        resulta += self.model.encode("\"").tolist()[0]
        fn_name_ids = constrained_function_name(self, fun_name_li, tokens)
        self.fn_name = self.model.decode(fn_name_ids)
        resulta += fn_name_ids
        resulta += self.model.encode("\"")[0].tolist()
        tokens += self.model.encode("\"")[0].tolist()
        tokens = get_word(self, ",\"parameters\":{", tokens)
        resulta = get_word(self, ",\"parameters\":{", resulta)
        para = get_fun_parametre(self.fn_name)
        num_para = len(para.keys())
        get_name_and_type(self, resulta, tokens, num_para, para, i)
        return tokens, resulta

    def main(self: Any) -> Any:
        result: list[int] = []
        r_final: list[int] = []
        for prompt in self.li_prompts:
            i = len(prompt)
            result = get_my_prompt(self, prompt)
            self.user_prt = prompt
            result, j = self.process(result, i)
            r_final += j
            self.start = 0
        r_final = get_brakcets(self, "end", r_final)
        return self.model.decode(r_final)
