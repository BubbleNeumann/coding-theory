import numpy as np
from lab1 import sub_lines, mul_vector_by_matrix
import random


def prepare_matrix(matrix) -> list:
    """
    transforms matrix to binary type
    """
    for i in range(len(matrix)):
        matrix[i] = list(map(lambda x: x % 2, matrix[i]))
    return matrix

def prepare_vector(vec) -> list:
    """
    function which transforms vector to binary type
    """
    return list(map(lambda x: x % 2, vec))

def row_sum(matrix, n) -> int:
    return sum(matrix[n])

def col_sum(matrix, n) -> int:
    res = 0
    for i in range(len(matrix)):
        res += matrix[i][n]
    return res



class LinearMatrix: 
    def __init__(self, rows:int =0, cols:int =0) -> None: 
        """ 
        creating a generator matrix (7, 4, 3) rows = 4, cols = 7, d = 3 
        """ 
        self.matrix = np.eye(4 if rows == cols == 0 else rows, dtype=int).tolist() 
        self.H = [] 
        if (rows == cols == 0):
            self.cols = 7 
            self.rows = 4 
            self.x_part = [[1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]] 
            for i in range(len(self.matrix)): 
                for j in range(len(self.x_part[0])): 
                    self.matrix[i].append(self.x_part[i][j]) 
        else:
            m = cols
            n = rows
            matrix = [[0 for i in range(m)] for j in range(n)]
            for j in matrix:
                print(j)
            o1,o2,o3,o4 = 0,0,0,0

            for i in range(n):
                for j in range(m):
                    if(i == j):
                        matrix[i][j] = 1
            arr_1 = []

            o1 = random.randint(n,m-1)
            arr_1.append(o1)
            while(True):
                o2 = random.randint(n,m-1)
                if(o1 != o2):
                    arr_1.append(o2)
                    break
            while(True):
                o3 = random.randint(n,m-1)
                if(o1 != o3 and o2 != o3):
                    arr_1.append(o3)
                    break
            while(True):
                o4 = random.randint(n,m-1)
                if(o1 != o4 and o2 != o4 and o3 != o4):
                    arr_1.append(o4)
                    break
            matrix[0][o1] = 1
            matrix[0][o2] = 1
            matrix[0][o3] = 1
            matrix[0][o4] = 1
            for i in range(1,n):
                while True:
                    k = 0
                    o1 = random.randint(n,m-1)
                    while(True):
                        o2 = random.randint(n,m-1)
                        if(o1 != o2):
                            break
                    while(True):
                        o3 = random.randint(n,m-1)
                        if(o1 != o3 and o2 != o3):
                            break
                    while(True):
                        o4 = random.randint(n,m-1)
                        if(o1 != o4 and o2 != o4 and o3 != o4):
                            break
                    if o1 in arr_1:
                        k += 1
                    if o2 in arr_1:
                        k += 1
                    if o3 in arr_1:
                        k += 1
                    if o4 in arr_1:
                        k += 1
                    if k == 2:
                        arr_1.append(o1)
                        arr_1.append(o2)
                        arr_1.append(o3)
                        arr_1.append(o4)
                        matrix[i][o1] = 1
                        matrix[i][o2] = 1
                        matrix[i][o3] = 1
                        matrix[i][o4] = 1
                        break
                self.cols = cols
                self.rows = rows
                
 
         
    def __str__(self) -> str: 
        print("number of cols: ", self.cols, " number of rows: ", self.rows) 
        for i in range(self.rows - 1): 
            print(self.matrix[i]) 
        return str(self.matrix[self.rows-1]) 
     
    def createCheckMatrix(self) -> list: 
        """ 
        creating a check matrix 
        """ 
        for i in self.x_part: 
            self.H.append(i) 
        j = np.eye(self.cols - self.rows, dtype=int).tolist() 
        for i in j: 
            self.H.append(i) 
        return self.H

    def gen_all_code_words(self) -> list:
        all_code_words = []
        for word in range(len(self.matrix)):
            for word1 in range(len(self.matrix)):
                all_code_words.append(sub_lines(matrix=self.matrix, ind_from=word, ind_what=word1)[word])
        return all_code_words

    def fix_word_with_one_mistake(self, word):
        mistake_ind = self.H.index(prepare_vector(mul_vector_by_matrix(word, self.H)))
        word[mistake_ind] = 1 if word[mistake_ind] == 0 else 0
        return word

    def fix_word_with_two_mistakes(self, word):
        def lists_are_equal(list1: list, list2: list):
            if len(list1) != len(list2):
                return False
            for i in range(len(list1)):
                if list1[i] != list2[i]:
                    return False
            return True

        two_dim_syndroms = self.gen_syndrom(dim=2)
        for i in range(len(two_dim_syndroms)):
            for j in range(i+1, len(two_dim_syndroms)):
                list1 = prepare_vector(mul_vector_by_matrix(word, self.H))
                list2 = two_dim_syndroms[i][j]
                if lists_are_equal(list1, list2):
                    word[i] = 1 if word[i] == 0 else 0
                    word[j] = abs(word[j]-1)
                    return word


    def word_form(n,word,numf = 2): #2.4, 2.5
        """
        gen code word of length = n out of word, with numf errors
        """
        word_new = [0]*n
        for i in range(n-len(word),n):
            word_new[i] = word[i- (n-len(word))]
        print(word_new)
        fool_1 = random.randint(0,n-1)
        while(True):
            fool_2 = random.randint(0,n-1)
            if(fool_1 != fool_2):
                break
        if(word_new[fool_1]):
            word_new[fool_1] = 0
        else:
            word_new[fool_1] = 1
        if(numf == 2):
            if(word_new[fool_2]):
                word_new[fool_2] = 0
            else:
                word_new[fool_2] = 1
        print("fool_1:", fool_1, "; fool_2: ", fool_2)
        return word_new

    @staticmethod
    def make_mistake(word, list_of_mistakes) -> list:
        """
        gen word with mistakes on posisions specified in list of mistakes
        """
        return [abs(x + y) for x, y in zip(word, list_of_mistakes)]


    def gen_syndrom(self, dim: int = 1) -> list: #2.3
        """
        dim = number of errors in word
        """
        if dim == 1:
            syndrom = [[0]*(self.cols-self.rows)]
            syndrom.extend(self.H)
            return syndrom
            
        code_word = self.gen_all_code_words()[1]
        syndrom = []

        for i in range(len(code_word)):
            syndrom_line = []
            for j in range(len(code_word)):
                if i >= j:
                    syndrom_line.append(0)
                    continue
                list_of_mistakes = [0]*len(code_word)
                list_of_mistakes[i] = 1
                list_of_mistakes[j] = 1
                syndrom_line.append(prepare_vector(mul_vector_by_matrix(LinearMatrix.make_mistake(code_word, list_of_mistakes), self.H)))
            syndrom.append(syndrom_line)

        return syndrom


def main():
    G = LinearMatrix()
    H = G.createCheckMatrix()
    code_word = G.gen_all_code_words()[2]
    mistake = [0]*len(code_word)
    mistake[0] = 1 # make mistake at the first pos
    print('code word=', code_word, 'code word with mistake=', LinearMatrix.make_mistake(code_word, mistake), 'fixed=', G.fix_word_with_one_mistake(LinearMatrix.make_mistake(code_word, mistake)))
    print('G=', G)
    print('H=', H)

    mistake[1] = 1
    print('code word=', code_word, 'code word with mistake=', prepare_vector(LinearMatrix.make_mistake(code_word, mistake)), 'fixed=', prepare_vector(G.fix_word_with_two_mistakes(LinearMatrix.make_mistake(code_word, mistake))))
    syndroms = G.gen_syndrom(dim=2)
    for row in syndroms:
        print(row)

if __name__ == '__main__':
    main()
