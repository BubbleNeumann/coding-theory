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

class LinearMatrix:
    def __init__(self) -> None:
        """
        creating a generator matrix
        """
        pass
        
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
    pass


if __name__ == 'main':
    main()