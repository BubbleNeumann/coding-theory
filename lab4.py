import numpy as np
import copy
from lab1 import mul_vector_by_matrix, prepare_vector

def attachHorizontal(M1, M2):
    M3 = []
    for i in range(0, len(M1)):
        m = []
        for j in range(0, len(M1[0]) + len(M2[0])):
            if j < len(M1[0]):
                m.append(M1[i][j])
            else:
                m.append(M2[i][j - len(M1[0])])
        M3.append(m)
    return M3

def attachVertical(M1, M2):
    M3 = copy.copy(M1)
    for m in M2:
        M3.append(m)
    return M3

def mulKron(A, C):
    a = np.array(A)
    c = np.array(C)
    return np.kron(A, C).tolist()

B = [[1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
     [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
     [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
     [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
     [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
     [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
     [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
     [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
     [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
     [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
     [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]

Kroneker = [[1, 1], [1, -1]]

class GoleyMatrix:
    def __init__(self) -> None:
        self.matrix = np.eye(12, dtype=int).tolist()
        for i in range(len(B)):
            for j in range(len(B[0])):
                self.matrix[i].append(B[i][j])
    
    def createCheckMatrix(self) -> None:
        self.H = np.eye(12, dtype=int).tolist()
        for i in range(len(B)):
            self.H.append(B[i])


def RM(r:int, m:int) -> list:
    if 0 < r < m:
        G11_2 = RM(r, m - 1)
        G22 = RM(r - 1, m - 1)
        G_left = attachVertical(G11_2, np.zeros((len(G22), len(G11_2[0])), dtype=int).tolist())
        G_right = attachVertical(G11_2, G22)
        return attachHorizontal(G_left, G_right)
    elif r == 0:
        return np.ones((1, 2 ** m), dtype=int).tolist()
    elif r == m:
        G_top = RM(r - 1, m)
        bottom_matrix = np.zeros((1, 2 ** m), dtype=int).tolist()
        bottom_matrix[0][len(bottom_matrix[0]) - 1] = 1
        return attachVertical(G_top, bottom_matrix)

class RmMatrix:
    def __init__(self, r:int, m:int) -> None:
        self.matrix = RM(r, m)

    def createCheckMatrix(self, i:int, m:int) -> list:
        I1 = np.eye(pow(2, m - i), dtype=int).tolist()
        I2 = np.eye(pow(2, i - 1), dtype=int).tolist()
        return mulKron(mulKron(I1, Kroneker), I2)
    
    @staticmethod
    def prepareWord(word: list) -> list:
        for i in range(len(word)):
            if word[i] == 0:
                word[i] = -1
        return word
    @staticmethod
    def find_max_j(vec: list) -> int:
        max_val = max(vec)
        min_val = min(vec)
        if abs(max_val) > abs(min_val):
            return vec.index(max_val)
        else:
            return vec.index(min_val)
    @staticmethod
    def decode_word(vec: list, mistake_pos: int, word_len: int) -> list:
        b = []
        n = copy.copy(mistake_pos)
        while n > 0:
            b.append(n % 2)
            n //= 2
        for i in range(word_len - 1 - len(b)):
            b.append(0)
        if vec[mistake_pos] > 0:
            b.insert(0, 1)
        else: 
            b.insert(0, 0)
        return b
def main():
    print("part 1: \n")
    G = GoleyMatrix()
    print("Goley matrix: ")
    for i in G.matrix:
        print(i)
    print("\n")
    G.createCheckMatrix()
    print("H matrix: ")
    for i in G.H:
        print(i)
    print("\n")

    print("part 2: \n")
    u = [1, 1, 0, 0]
    word_with_one_m = [1, 0, 1, 0, 1, 0, 1, 1]
    word_with_two_m = [1, 0, 1, 0, 1, 1, 1, 1]
    G = RmMatrix(1, 3)
    word = prepare_vector(mul_vector_by_matrix(u, G.matrix))
    print("RM matrix (1, 3): ")
    for i in G.matrix:
        print(i)
    print("\n")
    H1 = G.createCheckMatrix(1, 3)
    H2 = G.createCheckMatrix(2, 3)
    H3 = G.createCheckMatrix(3, 3)
    # print("H1 matrix: ")
    # for i in H1:
    #     print(i)

    # print("\nH2 matrix: ")
    # for i in H2:
    #     print(i)
    
    # print("\nH3 matrix: ")
    # for i in H3:
    #     print(i)
    print("right word before coding: ", u)
    print("right word: ", word)
    print("word with one mistake: ", word_with_one_m)
    word_with_one_m = RmMatrix.prepareWord(word_with_one_m)
    w1 = mul_vector_by_matrix(word_with_one_m, H1)
    w2 = mul_vector_by_matrix(w1, H2)
    w3 = mul_vector_by_matrix(w2, H3)
    print("\n w*H1= ", w1)
    print("w1*H2= ", w2)
    print("w2*H3= ", w3)
    mistake_pos = RmMatrix.find_max_j(w3)
    print("mistake position: ", mistake_pos)
    print("corrected word: ", RmMatrix.decode_word(w3, mistake_pos, 4))
    print("\nword with two mistakes: ", word_with_two_m)
    word_with_two_m = RmMatrix.prepareWord(word_with_two_m)
    w1 = mul_vector_by_matrix(word_with_two_m, H1)
    w2 = mul_vector_by_matrix(w1, H2)
    w3 = mul_vector_by_matrix(w2, H3)
    print("w*H1= ", w1)
    print("w1*H2= ", w2)
    print("w2*H3= ", w3)
    mistake_pos = RmMatrix.find_max_j(w3)
    print("mistake position: ", mistake_pos)
    print("corrected word: ", RmMatrix.decode_word(w3, mistake_pos, 4))
    u = [1, 1, 0, 0, 0]
    G = RmMatrix(1, 4)
    word = prepare_vector(mul_vector_by_matrix(u, G.matrix))
    word_with_one_m = [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    word_with_two_m = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    word_with_three_m = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    word_with_four_m = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
    print("RM matrix (1, 4): ")
    for i in G.matrix:
        print(i)
    print("\n")
    H1 = G.createCheckMatrix(1, 4)
    H2 = G.createCheckMatrix(2, 4)
    H3 = G.createCheckMatrix(3, 4)
    H4 = G.createCheckMatrix(4, 4)
    print("right word before coding: ", u)
    print("right word: ", word)
    print("word with one mistake: ", word_with_one_m)
    word_with_one_m = RmMatrix.prepareWord(word_with_one_m)
    w1 = mul_vector_by_matrix(word_with_one_m, H1)
    w2 = mul_vector_by_matrix(w1, H2)
    w3 = mul_vector_by_matrix(w2, H3)
    w4 = mul_vector_by_matrix(w3, H4)
    print("w*H1= ", w1)
    print("w1*H2= ", w2)
    print("w2*H3= ", w3)
    print("w3*H4= ", w4)
    mistake_pos = RmMatrix.find_max_j(w4)
    print("mistake position: ", mistake_pos)
    print("corrected word: ", RmMatrix.decode_word(w3, mistake_pos, 5))
    print("word with two mistakes: ", word_with_two_m)
    word_with_two_m = RmMatrix.prepareWord(word_with_two_m)
    w1 = mul_vector_by_matrix(word_with_two_m, H1)
    w2 = mul_vector_by_matrix(w1, H2)
    w3 = mul_vector_by_matrix(w2, H3)
    w4 = mul_vector_by_matrix(w3, H4)
    print("w*H1= ", w1)
    print("w1*H2= ", w2)
    print("w2*H3= ", w3)
    print("w3*H4= ", w4)
    mistake_pos = RmMatrix.find_max_j(w4)
    print("mistake position: ", mistake_pos)
    print("corrected word: ", RmMatrix.decode_word(w3, mistake_pos, 5))
    print("word with three mistakes: ", word_with_three_m)
    word_with_three_m = RmMatrix.prepareWord(word_with_three_m)
    w1 = mul_vector_by_matrix(word_with_three_m, H1)
    w2 = mul_vector_by_matrix(w1, H2)
    w3 = mul_vector_by_matrix(w2, H3)
    w4 = mul_vector_by_matrix(w3, H4)
    print("w*H1= ", w1)
    print("w1*H2= ", w2)
    print("w2*H3= ", w3)
    print("w3*H4= ", w4)
    mistake_pos = RmMatrix.find_max_j(w4)
    print("mistake position: ", mistake_pos)
    print("corrected word: ", RmMatrix.decode_word(w3, mistake_pos, 5))
    print("word with four mistakes: ", word_with_four_m)
    word_with_four_m = RmMatrix.prepareWord(word_with_four_m)
    w1 = mul_vector_by_matrix(word_with_four_m, H1)
    w2 = mul_vector_by_matrix(w1, H2)
    w3 = mul_vector_by_matrix(w2, H3)
    w4 = mul_vector_by_matrix(w3, H4)
    print("w*H1= ", w1)
    print("w1*H2= ", w2)
    print("w2*H3= ", w3)
    print("w3*H4= ", w4)
    mistake_pos = RmMatrix.find_max_j(w4)
    print("mistake position: ", mistake_pos)
    print("corrected word: ", RmMatrix.decode_word(w3, mistake_pos, 5))


if __name__ == '__main__':
    main()