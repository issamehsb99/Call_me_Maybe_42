# from typing import List


# def _count_vowels(s: str) -> int:
#     """Count vowels in a string, case-insensitively."""
#     return sum(1 for ch in s if ch.lower() in "aeiou")


# def _sort_key(s: str) -> tuple:
#     """Build the comparison key: (length, case-insensitive value, vowel count)."""
#     return (len(s), s.lower(), _count_vowels(s))


# def _merge(left: List[str], right: List[str]) -> List[str]:
#     """Merge two already-sorted lists, preserving stability on ties."""
#     result = []
#     i = j = 0
#     while i < len(left) and j < len(right):
#         # '<=' (not '<') keeps left-side elements first on ties -> stable
#         if _sort_key(left[i]) <= _sort_key(right[j]):
#             result.append(left[i])
#             i += 1
#         else:
#             result.append(right[j])
#             j += 1
#     result.extend(left[i:])
#     result.extend(right[j:])
#     return result


# def multi_criteria_sort(strings: List[str]) -> List[str]:
#     """Sort strings by length, then case-insensitive ASCII order, then vowel count.

#     Stable: equal elements keep their original relative order.
#     Does not use sorted() or list.sort().
#     """
#     if len(strings) <= 1:
#         return list(strings)
#     mid = len(strings) // 2
#     left = multi_criteria_sort(strings[:mid])
#     right = multi_criteria_sort(strings[mid:])
#     return _merge(left, right)

# if __name__ == "__main__":
#     data = ["banana", "Apple", "kiwi", "Fig", "Pear", "dog", "cat", "Ox"]
#     print(multi_criteria_sort(data))


def cryptic_sorter(strings: list[str]) -> list[str]:

    return sorted(strings, key=lambda x: (len(x), x.lower(), strings.index(x)))

# print(cryptic_sorter(["hello","world","hi","test"]))
# # def echo_validator(text: str) -> bool:


# def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
#     li = []
#     for i in matrix:
#         li.append(i[::-1])
#     return (li)


# print(mirror_matrix([[1, 2, 3],[4, 5, 6]]))
# i = int("255", 10)
# base = "0123456789abcdefghijklmnopqrstuvwxyz"
# res = []
# while i > 16:
#     i = i % 16
#     res.append(base[i])
# res.append(base[i])
# print("jj", res)
# print("".join(res))

# def twist_sequence(li:list, i :int)->list:
#     new = []
#     j = 0
#     if i < len(li):
#         while j < len(li):
#             new.append(li[-i])
#             i -=1 
#             j +=1
#     else :
#         i -= len(li)
#         while j < len(li):
#             print(i, "\n")
#             new.append(li[-i])
#             i -= 1 
#             j +=1
#     return new

# print(twist_sequence([1,2,3], 5))

# def string_sculptor(text: str)-> str:
#     i = 0
#     new = []
#     while i < len(text):
#         if text[i] in " ":
#             new.append(text[i])
#             i+=1
#             if i == len(text):
#                 break
#             else:
#                 new.append(text[i].lower())
#                 i+=1
#                 continue
#         if i == 0:
#             new.append(text[i].lower())
#             i +=1
#         if text[i].isalpha() :
#             new.append(text[i].upper())
#             i +=1
#             if i == len(text):
#                 break
#             new.append(text[i])
#             # print(i)
#         else :
#             new.append(text[i])
#             i+=1
#             continue
#         i +=1
#     print("".join(new))
# string_sculptor("Hello World")
# string_sculptor("hello")
# string_sculptor("abc123def")
def whisper_cipher(text:str , i :int)->str:
    for i in range(len(text)):
        if l