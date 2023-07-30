import numpy as np


def reverse_list(li):
    return li.sort(reverse=True)


l = [1, 2, 3, 4, 5]
reverse_list(l)
print(l)
