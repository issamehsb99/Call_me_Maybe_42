import numpy as np


def extract_token_n(ids, n):
    """that function extract token n from ids """
    chose = set()
    for i in ids:
        if len(i) > n:
            chose.add(i[n])
    return (chose)


def constrained_function_name(self, fun_name_li: list[list[int]], in_id: list[int]):
    just_copy = fun_name_li.copy()
    n = 0
    output = []
    while (True):
        logits = self.model.get_logits_from_input_ids(in_id)
        chosen = extract_token_n(just_copy, n)
        if not chosen:
            break
        filtred = np.full_like(logits, -np.inf)
        for t in chosen:
            filtred[t] = logits[t]
        next_token = int(np.argmax(filtred))
        in_id.append(next_token)
        output.append(next_token)
        chosen.remove(next_token)
        if (self.model.decode(np.argmax(logits)) == "\""):
            break
        just_copy = [
            p for p in just_copy
            if len(p) > n and p[n] == next_token
                    ]
        if any(n == len(p) for p in just_copy):
            break
        n += 1
    return output


def get_brakcets(self, state: str, tokens: list[int]):
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
