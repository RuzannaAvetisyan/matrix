from typing import Union
import math
import random


class InvalidMatrixError(TypeError):
    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


class NotSquareMatrixError(TypeError):
    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


class MatrixMathOperationError(ValueError):
    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


class Matrix:

    # 1.__ init__ (self, 2d_array) must get 2d array in argument
    def __init__(self, data: Union[list]):
        if not isinstance(data, list):
            raise TypeError(f'List expected {type(data)} found')

        if data:
            if not isinstance(data[0], list):
                raise TypeError(f'List expected {type(data[0])} found')

            columns = len(data[0])
            for row in data[0:]:
                if not isinstance(row, list):
                    raise TypeError(f'List expected {type(row)} found')

                for i in row:
                    if not isinstance(i, (int, float)):
                        raise TypeError(f'List expected {type(i)} found')

                if len(row) != columns:
                    raise InvalidMatrixError('inconsistent matrix structure', 'dimension')

        self._data = data

    # 2.__ add__(self, other_matrix) method should add current instance to matrix instanse that pass as argument
    def __add__(self, other_matrix):
        return self.__math_op__(other_matrix)

    # 3.__sub__(self, other_matrix) method should subtract from current instance a matrix instanse that pass as argument
    def __sub__(self, other_matrix):
        return self.__math_op__(other_matrix, add=False)

    def __math_op__(self, other_matrix, add=True):
        if not isinstance(other_matrix, Matrix):
            raise TypeError(f'List expected {type(other_matrix)} found')
        matrix_row_size = len(other_matrix._data)

        if self.same_dimension_with(other_matrix):
            raise MatrixMathOperationError('Impossible matrix operations', 'dimension')

        new_matrix = []

        for i in range(matrix_row_size):
            matrix_col_size = len(self._data[0])
            matrix_row = []
            for j in range(matrix_col_size):
                if add:
                    matrix_row.append(self._data[i][j] + other_matrix._data[i][j])
                else:
                    matrix_row.append(self._data[i][j] - other_matrix._data[i][j])
            new_matrix.append(matrix_row)

        return Matrix(new_matrix)

    # 4. __ mul__(self, other_matrix) method should multiply current instance with matrix instanse that pass as argument
    def __mul__(self, other_matrix):
        if not isinstance(other_matrix, Matrix):
            raise TypeError(f'List expected {type(other_matrix)} found')
        other_mrsize = len(other_matrix._data)
        if other_mrsize == 0 or len(self._data) == 0 or len(self._data[0]) != other_mrsize:
            raise MatrixMathOperationError('Impossible matrix operations', 'dimension')
        else:
            result = []
            for i in range(len(self._data)):
                row = []
                for j in range(len(other_matrix._data[0])):
                    res = 0
                    for k in range(other_mrsize):
                        res += self._data[i][k] * other_matrix._data[k][j]
                    row.append(res)
                result.append(row)
        return Matrix(result)

    # 5. __ str__(self, other_matrix) method shuld return string of matrix as follows:
    def __str__(self):
        print_matrix = ''
        if len(self._data) == 0:
            print_matrix = '[]'
        elif len(self._data) == 1:
            print_matrix = self._data[0].__str__
        else:
            m_size = len(self._data)
            for i in range(m_size):
                matrix_row = ''
                m_r_size = len(self._data[i])
                for j in range(m_r_size):
                    matrix_row += f'{self._data[i][j]}, '
                    if j == m_r_size - 1:
                        matrix_row = matrix_row[:-2]
                if i == 0:
                    print_matrix = f'⌈{matrix_row}⌉\n'
                elif i == m_size - 1:
                    print_matrix += f'⌊{matrix_row}⌋\n'
                else:
                    print_matrix += f'|{matrix_row}|\n'
        return print_matrix

    def get_cofactor(self, i, j):
        return Matrix([row[: j] + row[j + 1:] for row in (self._data[: i] + self._data[i + 1:])])

    # 6. determinant() calculates determinant of matrix
    def determinant(self):
        if self.is_square() and len(self._data) > 1:
            if len(self._data) == 2:
                value = self._data[0][0] * self._data[1][1] - self._data[1][0] * self._data[0][1]
                return value
            det = 0

            for current_column in range(len(self._data)):
                sign = (-1) ** current_column
                sub_det = self.get_cofactor(0, current_column).determinant()
                det += (sign * self._data[0][current_column] * sub_det)

            return det
        else:
            raise NotSquareMatrixError('Impossible matrix operations', 'Matrix is not square')

    # 7. inverse() calculate inverse of matrix
    def inverse(self):
        if self.is_square() and self.determinant() != 0:
            inverse = []
            for i in range(len(self._data)):
                row = []
                for j in range(len(self._data[0])):
                    row.append(math.pow(-1, (i+j)) * self.get_cofactor(i, j).determinant())
                inverse.append(row)
            det = 1 / self.determinant()
            adjugate = list(zip(*inverse))
            for i in range(len(self._data)):
                for j in range(len(self._data[0])):
                    inverse[i][j] = adjugate[i][j] * det
            return Matrix(inverse)
        else:
            raise MatrixMathOperationError('Impossible matrix operations', 'dimension or determinant = 0')

    # 8 . same_dimention_with(other_matrix) makes sure other matrix has the same dimension as instance matrix
    def same_dimension_with(self, other_matrix):
        if len(self._data) != len(other_matrix._data):
            return False
        elif len(self._data) != 0 and len(self._data[0]) != len(other_matrix._data[0]):
            return False
        else:
            return True

    # 9. is_square() check if matrix is square
    def is_square(self):
        if self._data:
            if len(self._data) == len(self._data[0]):
                return True
            else:
                return False
        else:
            return False

    # 10. random_matrix() static method returns instance of Matrix by
    @staticmethod
    def random_matrix():
        matrix = []
        m_row = random.randint(1, 10)
        m_col = random.randint(1, 10)
        for i in range(m_row):
            row = []
            for j in range(m_col):
                row.append(random.randint(1, 100))
            matrix.append(row)
        return Matrix(matrix)


if __name__ == '__main__':
    print(Matrix.random_matrix())


