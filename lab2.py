import numpy as np

def prepare_matrix(matrix) -> list:
    """
    function which transforms matrix to binary type
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
    def __init__(self) -> None:
        """
        creating a generator matrix (7, 4, 3) rows = 4, cols = 7, d = 3
        """
        self.matrix = np.eye(4).tolist() # единичная матрица k х k размера
        x_part = np.zeros((4, 3), dtype=int).tolist()
        for i in range(len(x_part)):
            if i > 1:
                for j in range(len(x_part[0])):
                    if row_sum(x_part, i) < 2 and col_sum(x_part, j) < 2:
                        x_part[i][j] = 1
            else:
                x_part[i][i] = 1
                x_part[i][i+1] = 1
        print(x_part)
        for i in range(len(self.matrix)):
            for j in range(len(x_part[0])):
                self.matrix[i].append(x_part[i][j])
        print(self.matrix)
        

        
    def __str__(self) -> str:
        return " "
    
    def createCheckMatrix(self) -> list:
        """
        creating a check matrix
        """
        pass

    def createSyndromeTable(self) -> list:
        """
        generate a table of syndromes for all single errors.
        """
        pass



def main():
    a = LinearMatrix()


# if __name__ == 'main':
#     main()

main()