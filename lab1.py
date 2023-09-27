import numpy

def sub_lines(matrix, ind_from: int, ind_what: int) -> list:
    """
    subtracts lines
    """
    matrix[ind_from] = list(map(lambda x, y: abs(x-y), matrix[ind_from], matrix[ind_what]))
    return matrix

def get_code_offset(matrix, ind_from: int, ind_what: int) -> list:
    """
    returns the distance between all lines
    """
    matrix[ind_from] = list(map(lambda x, y: abs(x-y), matrix[ind_from], matrix[ind_what]))
    return len(list(filter(lambda a: a !=1, matrix[ind_from])))


def should_sub(matrix, ind_from, leading_1_col) -> bool:
    """
    performs a check for the need to subtract a string
    """
    return matrix[ind_from][leading_1_col] == 1


def ref(arr) -> list:
    t = 0
    mass = []
    for i in arr:
        for j in arr:
            if i < j:
                t += 1
        mass.append(t)
        t = 0
    rez = [[]]*len(mass)
    for i in range(len(mass)):
        rez[mass[i]] = arr[i]
    return rez


def rref(matrix) -> list:
    for row_ind in range(len(matrix)):
        leading_1 = 0
        while matrix[row_ind][leading_1] != 1:
            leading_1 += 1
        for row_ind_1 in range(row_ind):
            if should_sub(matrix, row_ind_1, leading_1):
                matrix = sub_lines(matrix, row_ind_1, row_ind)
    return matrix


def prepare_matrix(matrix) -> list:
    """
    function which transforms matrix to binary type
    """
    for i in range(len(matrix)):
        matrix[i] = list(map(lambda x: x % 2, matrix[i]))
    return matrix

def prepare_vector(vec) -> list:
    return list(map(lambda x: x % 2, vec))

def mul_vector_by_matrix(vector, matrix) -> list:
    np_vec = numpy.array(vector)
    np_matrix = numpy.array(matrix)
    return (np_vec.dot(np_matrix)).tolist()


class LinearCode:
    def __init__(self, matrix) -> None:
        self.matrix = prepare_matrix(matrix)  # base matrix 
        self.cols = len(matrix[0])  # number of cols
        self.rows = len(matrix)  # number of rows

    def s_ref(self) -> None:
        """
        transforms matrix to the upper-triangular form
        """
        t = 0
        mass = []
        for i in self.matrix:
            for j in self.matrix:
                if i < j:
                    t += 1
            mass.append(t)
        t = 0
        rez = [[]]*len(mass)
        for i in range(len(mass)):
            rez[mass[i]] = self.matrix[i]
        self.matrix = rez

    def s_rref(self) -> None:
        """
        transforms matrix to the reduced upper - triangular form
        """
        for row_ind in range(len(self.matrix)):
            leading_1 = 0
        while self.matrix[row_ind][leading_1] != 1:
            leading_1 += 1
        for row_ind_1 in range(row_ind):
            if should_sub(self.matrix, row_ind_1, leading_1):
                self.matrix = sub_lines(self.matrix, row_ind_1, row_ind)

    def get_leading_1s(self) -> list:
        """
        returns list of leadings cols
        """
        res = []
        for row_ind in range(len(self.matrix)):
            leading_1 = 0
            while self.matrix[row_ind][leading_1] != 1:
                leading_1 += 1
            res.append(leading_1)
        return res


    def f_ilya(self) -> list:
        """
        get X matrix
        """
        arr = self.get_leading_1s()
        print(arr)
        rez = []
        temp = [[]]*self.rows
        door = False
        for i in range(self.rows):
            for j in range(self.cols):
                for k in range(len(arr)):
                    if(arr[k] == j):
                        door = True
                        break
                    else:
                        continue
                if(door):
                    door = False
                    continue
                rez.append(self.matrix[i][j])
            temp[i] = rez
            rez = []
        return(temp)


    def get_check_matrix(self) -> list:
        """
        get H matrix
        """
        X = self.f_ilya()
        I = numpy.eye(len(X[0]), dtype=int).tolist()
        h = []
        leading_1 = self.get_leading_1s()
        cur_x = 0
        cur_i = 0
        for i in range(len(X)+len(I)):
            if i in leading_1:
                h.append(X[cur_x])
                cur_x +=1 
            else:
                h.append(I[cur_i])
                cur_i += 1
            # h.append(X[i] if i in leading_1 else I[i])
        return h


    def get_min_code_offset(self) -> int:
        """
        returns the minimum distance between lines
        """
        res = []
        for row_ind in range(self.rows):
            for row_ind_1 in range(row_ind+1, self.rows):
                res.append(get_code_offset(self.matrix, row_ind, row_ind_1))
        return min(res)


    def __str__(self) -> str:
        print("number of cols: ", self.cols, " number of rows: ", self.rows)
        for i in range(self.rows - 1):
            print(self.matrix[i])
        return str(self.matrix[self.rows-1])


def main():
    # inp =  [[1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    #         [0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
    #         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]

    inp =  [[5, 0, 3, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 2, 1, 0, 1, 1, 0, 0, 1, 9],
            [0, 0, 4, 0, 1, 0, 0, 1, 0, 0, 3],
            [0, 0, 0, 2, 0, 0, 1, 0, 0, 1, 6],
            [0, 0, 0, 0, 4, 6, 0, 0, 1, 5, 1]]


    lc = LinearCode(inp)
    lc.s_ref()
    lc.s_rref()
    print(lc)
    # print(lc.get_leading_1s())
    # get_code_offset(lc.matrix, 0, 1)
    # print(i for i in lc.get_check_matrix())
    for i in lc.get_check_matrix():
        print(i)

    word_with_error = [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0]
    word = [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0]

    print(mul_vector_by_matrix(word, lc.get_check_matrix()))
    print(mul_vector_by_matrix(word_with_error, lc.get_check_matrix()))


    # print(lc.get_min_code_offset())


if __name__ == '__main__':
    main()
