import numpy as np

def get_Kompl_matrix(I: list, m: int) -> list:
    res = []
    for i in range(m):
        if i not in I:
            res.append(i)
    return res

class RMmatrix:
    def __init__(self, r, m):
        self.r = r
        self.m = m
        self.matrix = []
        pass

    def decode(self, word: list):
        size = len(self.matrix)
        max_weight = pow(2, self.m - self.r - 1) - 1
        index = 0

        pass

    def check_decoded(self):
        pass


