import numpy as np
import copy



class HammingMatrix:
    def __init__(self, rank: int):
        self.rows = 2 ** rank - rank - 1
        self.cols = 2 ** rank - 1
        self.matrix = np.eye(self.rows, dtype=int).tolist()
        self.x_part = []
        self.H = []
        x = []
        for i in range(0, self.cols - self.rows):
            x.append(0)
        flag = True
        while flag:
            flag = False
            for j in range(0, len(x)):
                if x[len(x) - j - 1] == 0:
                    x[len(x) - j - 1] = 1
                    break
                else:
                    x[len(x) - j - 1] = 0
            if (sum(x) > 1):
                self.x_part.append(copy.copy(x))
            if len(self.x_part) != self.rows:
                flag = True
        for i in range(len(self.matrix)): 
                for j in range(len(self.x_part[0])): 
                    self.matrix[i].append(self.x_part[i][j]) 

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


def main():
    print("part 1: \n")
    G = HammingMatrix(3)
    print("Generated matrix: \n")
    for i in G.matrix:
        print(i)
    print("\n")
    H = G.createCheckMatrix()
    print("H matrix: \n")
    for i in H:
        print(i)
    print("\n")

if __name__ == '__main__':
    main()