import numpy as np
import random
from code_validators import validate_code_answer as shared_validate_code_answer
from engine import run_game_session, run_with_replay
from game_common import pick_true_false_statement

"""
Matrix Challenge - Solve matrix operations and transformations

This game challenges you to:
- Create 2D arrays (matrices)
- Perform matrix operations (addition, multiplication)
- Understand matrix properties (transpose, shape)
- Reshape matrices
- Work with matrix math
"""


def generate_create_matrix_challenge(difficulty="easy"):
    """Generate challenge to create a matrix"""
    question_type = random.choice(["zeros", "ones", "identity", "random", "full"])
    
    if difficulty == "easy":
        if question_type == "zeros":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            question = f"Write the code to create a {rows}x{cols} matrix of zeros"
            answer = f"np.zeros(({rows}, {cols}))"
        elif question_type == "ones":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            question = f"Write the code to create a {rows}x{cols} matrix of ones"
            answer = f"np.ones(({rows}, {cols}))"
        elif question_type == "identity":
            size = random.randint(2, 4)
            question = f"Write the code to create a {size}x{size} identity matrix"
            answer = f"np.eye({size})"
        elif question_type == "random":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            question = f"Write the code to create a {rows}x{cols} matrix with random integers from 0 to 9"
            answer = f"np.random.randint(0, 10, size=({rows}, {cols}))"
        else:  # full
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            value = random.randint(1, 5)
            question = f"Write the code to create a {rows}x{cols} matrix filled with {value}"
            answer = f"np.full(({rows}, {cols}), {value})"
        hint = "NumPy has functions to create matrices: zeros, ones, eye, full"
    elif difficulty == "medium":
        if question_type == "zeros":
            rows = random.randint(3, 6)
            cols = random.randint(3, 6)
            question = f"Write the code to create a {rows}x{cols} matrix of zeros"
            answer = f"np.zeros(({rows}, {cols}))"
        elif question_type == "ones":
            rows = random.randint(3, 6)
            cols = random.randint(3, 6)
            question = f"Write the code to create a {rows}x{cols} matrix of ones"
            answer = f"np.ones(({rows}, {cols}))"
        elif question_type == "identity":
            size = random.randint(3, 6)
            question = f"Write the code to create a {size}x{size} identity matrix"
            answer = f"np.eye({size})"
        elif question_type == "random":
            rows = random.randint(3, 6)
            cols = random.randint(3, 6)
            low = random.randint(0, 5)
            high = random.randint(10, 20)
            question = f"Write the code to create a {rows}x{cols} matrix with random integers from {low} to {high-1}"
            answer = f"np.random.randint({low}, {high}, size=({rows}, {cols}))"
        else:  # full
            rows = random.randint(3, 6)
            cols = random.randint(3, 6)
            value = random.randint(1, 10)
            question = f"Write the code to create a {rows}x{cols} matrix filled with {value}"
            answer = f"np.full(({rows}, {cols}), {value})"
        hint = "Matrix creation functions take shape as a tuple (rows, cols)"
    else:  # hard
        if question_type == "zeros":
            rows = random.randint(4, 8)
            cols = random.randint(4, 8)
            dtype = random.choice(["int", "float"])
            question = f"Write the code to create a {rows}x{cols} matrix of zeros with dtype {dtype}"
            answer = f"np.zeros(({rows}, {cols}), dtype=np.{dtype})"
        elif question_type == "ones":
            rows = random.randint(4, 8)
            cols = random.randint(4, 8)
            dtype = random.choice(["int", "float"])
            question = f"Write the code to create a {rows}x{cols} matrix of ones with dtype {dtype}"
            answer = f"np.ones(({rows}, {cols}), dtype=np.{dtype})"
        elif question_type == "identity":
            size = random.randint(4, 8)
            question = f"Write the code to create a {size}x{size} identity matrix"
            answer = f"np.eye({size})"
        elif question_type == "random":
            rows = random.randint(4, 8)
            cols = random.randint(4, 8)
            low = random.randint(-10, 0)
            high = random.randint(20, 50)
            question = f"Write the code to create a {rows}x{cols} matrix with random integers from {low} to {high-1}"
            answer = f"np.random.randint({low}, {high}, size=({rows}, {cols}))"
        else:  # full
            rows = random.randint(4, 8)
            cols = random.randint(4, 8)
            value = random.randint(1, 20)
            dtype = random.choice(["int", "float"])
            question = f"Write the code to create a {rows}x{cols} matrix filled with {value} (dtype {dtype})"
            answer = f"np.full(({rows}, {cols}), {value}, dtype=np.{dtype})"
        hint = "You can specify dtype parameter for matrix creation functions"
    
    return {"type": "create_matrix", "question": question, "answer": answer, "hint": hint}


def generate_matrix_math_challenge(difficulty="easy"):
    """Generate challenge for matrix arithmetic"""
    question_type = random.choice(["add", "subtract", "multiply", "dot", "scalar"])
    
    if difficulty == "easy":
        if question_type == "add":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix1 = np.random.randint(0, 10, size=(rows, cols))
            matrix2 = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to add them"
            answer = "np.add(matrix1, matrix2)"
        elif question_type == "subtract":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix1 = np.random.randint(5, 15, size=(rows, cols))
            matrix2 = np.random.randint(0, 5, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to subtract matrix2 from matrix1"
            answer = "np.subtract(matrix1, matrix2)"
        elif question_type == "multiply":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix1 = np.random.randint(0, 10, size=(rows, cols))
            matrix2 = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to multiply them element-wise"
            answer = "np.multiply(matrix1, matrix2)"
        elif question_type == "dot":
            rows1 = random.randint(2, 3)
            cols1 = random.randint(2, 3)
            rows2 = cols1
            cols2 = random.randint(2, 3)
            matrix1 = np.random.randint(0, 10, size=(rows1, cols1))
            matrix2 = np.random.randint(0, 10, size=(rows2, cols2))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to compute matrix multiplication (dot product)"
            answer = "np.dot(matrix1, matrix2)"
        else:  # scalar
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(rows, cols))
            scalar = random.randint(2, 5)
            question = f"Given: matrix = \n{matrix}\nWrite the code to multiply it by scalar {scalar}"
            answer = f"np.multiply(matrix, {scalar})"
        hint = "Matrix addition/subtraction requires same shape. Use np.dot() for matrix multiplication"
    elif difficulty == "medium":
        if question_type == "add":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix1 = np.random.randint(0, 20, size=(rows, cols))
            matrix2 = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to add them"
            answer = "np.add(matrix1, matrix2)"
        elif question_type == "subtract":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix1 = np.random.randint(10, 30, size=(rows, cols))
            matrix2 = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to subtract matrix2 from matrix1"
            answer = "np.subtract(matrix1, matrix2)"
        elif question_type == "multiply":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix1 = np.random.randint(0, 20, size=(rows, cols))
            matrix2 = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to multiply them element-wise"
            answer = "np.multiply(matrix1, matrix2)"
        elif question_type == "dot":
            rows1 = random.randint(3, 4)
            cols1 = random.randint(3, 4)
            rows2 = cols1
            cols2 = random.randint(3, 4)
            matrix1 = np.random.randint(0, 20, size=(rows1, cols1))
            matrix2 = np.random.randint(0, 20, size=(rows2, cols2))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to compute matrix multiplication"
            answer = "np.dot(matrix1, matrix2)"
        else:  # scalar
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(rows, cols))
            scalar = random.randint(2, 10)
            question = f"Given: matrix = \n{matrix}\nWrite the code to multiply it by scalar {scalar}"
            answer = f"np.multiply(matrix, {scalar})"
        hint = "For matrix multiplication, columns of first must equal rows of second"
    else:  # hard
        if question_type == "add":
            rows = random.randint(4, 6)
            cols = random.randint(4, 6)
            matrix1 = np.random.randint(0, 50, size=(rows, cols))
            matrix2 = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to add them"
            answer = "np.add(matrix1, matrix2)"
        elif question_type == "subtract":
            rows = random.randint(4, 6)
            cols = random.randint(4, 6)
            matrix1 = np.random.randint(20, 50, size=(rows, cols))
            matrix2 = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to subtract matrix2 from matrix1"
            answer = "np.subtract(matrix1, matrix2)"
        elif question_type == "multiply":
            rows = random.randint(4, 6)
            cols = random.randint(4, 6)
            matrix1 = np.random.randint(0, 50, size=(rows, cols))
            matrix2 = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to multiply them element-wise"
            answer = "np.multiply(matrix1, matrix2)"
        elif question_type == "dot":
            rows1 = random.randint(4, 6)
            cols1 = random.randint(4, 6)
            rows2 = cols1
            cols2 = random.randint(4, 6)
            matrix1 = np.random.randint(0, 50, size=(rows1, cols1))
            matrix2 = np.random.randint(0, 50, size=(rows2, cols2))
            question = f"Given: matrix1 = \n{matrix1}\nmatrix2 = \n{matrix2}\nWrite the code to compute matrix multiplication"
            answer = "np.dot(matrix1, matrix2)"
        else:  # scalar
            rows = random.randint(4, 6)
            cols = random.randint(4, 6)
            matrix = np.random.randint(0, 50, size=(rows, cols))
            scalar = random.randint(2, 20)
            question = f"Given: matrix = \n{matrix}\nWrite the code to multiply it by scalar {scalar}"
            answer = f"np.multiply(matrix, {scalar})"
        hint = "Matrix operations: add/subtract need same shape, dot product needs compatible dimensions"
    
    return {"type": "matrix_math", "question": question, "answer": answer, "hint": hint}


def generate_transpose_challenge(difficulty="easy"):
    """Generate challenge about matrix transpose"""
    question_type = random.choice(["transpose", "T", "property"])
    
    if difficulty == "easy":
        if question_type == "transpose":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get its transpose"
            answer = "np.transpose(matrix)"
        elif question_type == "T":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to transpose it"
            answer = "matrix.T"
        else:  # property
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            question = f"If a matrix has shape ({rows}, {cols}), what is the shape of its transpose?\nWrite as a tuple"
            answer = f"({cols}, {rows})"
        hint = "What happens to rows and columns when you transpose?"
    elif difficulty == "medium":
        if question_type == "transpose":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get its transpose"
            answer = "np.transpose(matrix)"
        elif question_type == "T":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to transpose it"
            answer = "matrix.T"
        else:  # property
            rows = random.randint(3, 6)
            cols = random.randint(3, 6)
            question = f"If a matrix has shape ({rows}, {cols}), what is the shape of its transpose?\nWrite as a tuple"
            answer = f"({cols}, {rows})"
        hint = "Transpose interchanges the dimensions"
    else:  # hard
        if question_type == "transpose":
            rows = random.randint(4, 7)
            cols = random.randint(4, 7)
            matrix = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get its transpose"
            answer = "np.transpose(matrix)"
        elif question_type == "T":
            rows = random.randint(4, 7)
            cols = random.randint(4, 7)
            matrix = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to transpose it"
            answer = "matrix.T"
        else:  # property
            rows = random.randint(4, 8)
            cols = random.randint(4, 8)
            question = f"If a matrix has shape ({rows}, {cols}), what is the shape of its transpose?\nWrite as a tuple"
            answer = f"({cols}, {rows})"
        hint = "What transformation does transpose perform on the shape?"
    
    return {"type": "transpose", "question": question, "answer": answer, "hint": hint}


def generate_matrix_shape_challenge(difficulty="easy"):
    """Generate challenge about matrix shape"""
    question_type = random.choice(["shape", "size", "ndim"])
    
    if difficulty == "easy":
        if question_type == "shape":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get its shape"
            answer = "matrix.shape"
        elif question_type == "size":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get the total number of elements"
            answer = "matrix.size"
        else:  # ndim
            matrix = np.random.randint(0, 10, size=(random.randint(2, 4), random.randint(2, 4)))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get the number of dimensions"
            answer = "matrix.ndim"
        hint = "matrix.shape returns (rows, cols), matrix.size returns total elements"
    elif difficulty == "medium":
        if question_type == "shape":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get its shape"
            answer = "matrix.shape"
        elif question_type == "size":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get the total number of elements"
            answer = "matrix.size"
        else:  # ndim
            matrix = np.random.randint(0, 20, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get the number of dimensions"
            answer = "matrix.ndim"
        hint = "Shape is a tuple, size is a scalar, ndim is the number of dimensions"
    else:  # hard
        if question_type == "shape":
            rows = random.randint(4, 7)
            cols = random.randint(4, 7)
            matrix = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get its shape"
            answer = "matrix.shape"
        elif question_type == "size":
            rows = random.randint(4, 7)
            cols = random.randint(4, 7)
            matrix = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get the total number of elements"
            answer = "matrix.size"
        else:  # ndim
            matrix = np.random.randint(0, 50, size=(random.randint(4, 7), random.randint(4, 7)))
            question = f"Given: matrix = \n{matrix}\nWrite the code to get the number of dimensions"
            answer = "matrix.ndim"
        hint = "For 2D matrices, ndim is 2, shape is (rows, cols), size is rows * cols"
    
    return {"type": "matrix_shape", "question": question, "answer": answer, "hint": hint}


def generate_reshape_matrix_challenge(difficulty="easy"):
    """Generate challenge to reshape a matrix"""
    question_type = random.choice(["reshape", "flatten", "ravel"])
    
    if difficulty == "easy":
        if question_type == "reshape":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            total = rows * cols
            new_rows = random.choice([i for i in range(2, total//2 + 1) if total % i == 0])
            new_cols = total // new_rows
            matrix = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to reshape it to ({new_rows}, {new_cols})"
            answer = f"matrix.reshape(({new_rows}, {new_cols}))"
        elif question_type == "flatten":
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to flatten it to 1D"
            answer = "matrix.flatten()"
        else:  # ravel
            rows = random.randint(2, 4)
            cols = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to flatten it to 1D (ravel)"
            answer = "matrix.ravel()"
        hint = "reshape() changes shape, flatten() and ravel() convert to 1D"
    elif difficulty == "medium":
        if question_type == "reshape":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            total = rows * cols
            new_rows = random.choice([i for i in range(2, total//2 + 1) if total % i == 0])
            new_cols = total // new_rows
            matrix = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to reshape it to ({new_rows}, {new_cols})"
            answer = f"matrix.reshape(({new_rows}, {new_cols}))"
        elif question_type == "flatten":
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to flatten it to 1D"
            answer = "matrix.flatten()"
        else:  # ravel
            rows = random.randint(3, 5)
            cols = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to flatten it to 1D (ravel)"
            answer = "matrix.ravel()"
        hint = "reshape() requires same total elements, flatten() returns copy, ravel() returns view"
    else:  # hard
        if question_type == "reshape":
            rows = random.randint(4, 6)
            cols = random.randint(4, 6)
            total = rows * cols
            new_rows = random.choice([i for i in range(2, total//2 + 1) if total % i == 0])
            new_cols = total // new_rows
            matrix = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to reshape it to ({new_rows}, {new_cols})"
            answer = f"matrix.reshape(({new_rows}, {new_cols}))"
        elif question_type == "flatten":
            rows = random.randint(4, 6)
            cols = random.randint(4, 6)
            matrix = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to flatten it to 1D"
            answer = "matrix.flatten()"
        else:  # ravel
            rows = random.randint(4, 6)
            cols = random.randint(4, 6)
            matrix = np.random.randint(0, 50, size=(rows, cols))
            question = f"Given: matrix = \n{matrix}\nWrite the code to flatten it to 1D (ravel)"
            answer = "matrix.ravel()"
        hint = "reshape() can use -1 for one dimension, flatten() always returns copy, ravel() returns view when possible"
    
    return {"type": "reshape_matrix", "question": question, "answer": answer, "hint": hint}


def generate_matrix_properties_challenge(difficulty="easy"):
    """Generate challenge about matrix properties"""
    question_type = random.choice(["symmetric", "identity", "square", "diagonal"])
    
    if difficulty == "easy":
        if question_type == "symmetric":
            size = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(size, size))
            # Make it symmetric
            matrix = (matrix + matrix.T) // 2
            question = f"Given: matrix = \n{matrix}\nWrite the code to check if it's symmetric (matrix == matrix.T)"
            answer = "np.array_equal(matrix, matrix.T)"
        elif question_type == "identity":
            size = random.randint(2, 4)
            question = f"Write the code to create a {size}x{size} identity matrix"
            answer = f"np.eye({size})"
        elif question_type == "square":
            size = random.randint(2, 4)
            matrix = np.random.randint(0, 10, size=(size, size))
            question = f"Given: matrix = \n{matrix}\nWrite the code to check if it's square (rows == cols)"
            answer = "matrix.shape[0] == matrix.shape[1]"
        else:  # diagonal
            size = random.randint(2, 4)
            matrix = np.eye(size) * np.random.randint(1, 10, size=size)
            question = f"Given: matrix = \n{matrix}\nWrite the code to extract the diagonal elements"
            answer = "np.diag(matrix)"
        hint = "Symmetric matrices equal their transpose, identity matrices have 1s on diagonal"
    elif difficulty == "medium":
        if question_type == "symmetric":
            size = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(size, size))
            matrix = (matrix + matrix.T) // 2
            question = f"Given: matrix = \n{matrix}\nWrite the code to check if it's symmetric"
            answer = "np.array_equal(matrix, matrix.T)"
        elif question_type == "identity":
            size = random.randint(3, 5)
            question = f"Write the code to create a {size}x{size} identity matrix"
            answer = f"np.eye({size})"
        elif question_type == "square":
            size = random.randint(3, 5)
            matrix = np.random.randint(0, 20, size=(size, size))
            question = f"Given: matrix = \n{matrix}\nWrite the code to check if it's square"
            answer = "matrix.shape[0] == matrix.shape[1]"
        else:  # diagonal
            size = random.randint(3, 5)
            matrix = np.eye(size) * np.random.randint(1, 20, size=size)
            question = f"Given: matrix = \n{matrix}\nWrite the code to extract the diagonal elements"
            answer = "np.diag(matrix)"
        hint = "np.diag() extracts diagonal, np.eye() creates identity matrix"
    else:  # hard
        if question_type == "symmetric":
            size = random.randint(4, 6)
            matrix = np.random.randint(0, 50, size=(size, size))
            matrix = (matrix + matrix.T) // 2
            question = f"Given: matrix = \n{matrix}\nWrite the code to check if it's symmetric"
            answer = "np.array_equal(matrix, matrix.T)"
        elif question_type == "identity":
            size = random.randint(4, 6)
            question = f"Write the code to create a {size}x{size} identity matrix"
            answer = f"np.eye({size})"
        elif question_type == "square":
            size = random.randint(4, 6)
            matrix = np.random.randint(0, 50, size=(size, size))
            question = f"Given: matrix = \n{matrix}\nWrite the code to check if it's square"
            answer = "matrix.shape[0] == matrix.shape[1]"
        else:  # diagonal
            size = random.randint(4, 6)
            matrix = np.eye(size) * np.random.randint(1, 50, size=size)
            question = f"Given: matrix = \n{matrix}\nWrite the code to extract the diagonal elements"
            answer = "np.diag(matrix)"
        hint = "Symmetric: A = A^T, Identity: 1s on diagonal, Square: rows == cols"
    
    return {"type": "matrix_properties", "question": question, "answer": answer, "hint": hint}


def generate_true_false_challenge(difficulty="easy", *, used_questions=None):
    """Generate true/false questions about matrix operations."""
    statements_by_difficulty = {
        "easy": [
            ("True or False: np.zeros((3, 4)) creates a 3x4 matrix filled with zeros.", "true"),
            ("True or False: Matrix addition requires both matrices to have the same shape.", "true"),
            ("True or False: Transposing a (3, 4) matrix gives a (4, 3) matrix.", "true"),
            ("True or False: matrix.shape returns a tuple (rows, cols).", "true"),
            ("True or False: You can reshape a (2, 6) matrix to (3, 4) because both have 12 elements.", "true"),
            ("True or False: np.ones((2, 3)) contains exactly 5 elements.", "false"),
            ("True or False: Transposing a matrix removes one row from the data.", "false"),
        ],
        "medium": [
            ("True or False: np.eye(5) creates a 5x5 identity matrix.", "true"),
            ("True or False: np.multiply(a, b) performs element-wise multiplication, not matrix multiplication.", "true"),
            ("True or False: matrix.T and np.transpose(matrix) are equivalent for 2D arrays.", "true"),
            ("True or False: matrix.size returns the total number of elements (rows * cols).", "true"),
            ("True or False: reshape() requires the total number of elements to remain the same.", "true"),
            ("True or False: A symmetric matrix equals its transpose.", "true"),
            ("True or False: For np.dot(a, b) to work, the number of columns in a must equal the number of rows in b.", "true"),
            ("True or False: Element-wise operations require matrices to have the same shape.", "true"),
            ("True or False: An identity matrix has 1s on the diagonal and 0s elsewhere.", "true"),
            ("True or False: For 2D matrices a and b, np.dot(a, b) gives the same result as a * b.", "false"),
            ("True or False: reshape() can change a matrix so it has a different total number of elements.", "false"),
        ],
        "hard": [
            ("True or False: np.full((3, 4), 5) creates a 3x4 matrix filled with 5s.", "true"),
            ("True or False: np.dot(a, b) performs matrix multiplication (not element-wise).", "true"),
            ("True or False: Transposing twice returns the original matrix.", "true"),
            ("True or False: matrix.ndim returns the number of dimensions (2 for a matrix).", "true"),
            ("True or False: You can use -1 in reshape to automatically calculate one dimension.", "true"),
            ("True or False: np.array_equal(matrix, matrix.T) checks if a matrix is symmetric.", "true"),
            ("True or False: Matrix multiplication is not commutative (A @ B ≠ B @ A in general).", "true"),
            ("True or False: Element-wise multiplication with * is different from matrix multiplication with @.", "true"),
            ("True or False: NumPy can broadcast a scalar to multiply with a matrix element-wise.", "true"),
            ("True or False: Multiplying any matrix by an identity matrix of compatible size returns the original matrix.", "true"),
            ("True or False: matrix.flatten() always returns a view sharing memory with the original matrix.", "false"),
            ("True or False: For any two square matrices A and B of the same shape, A @ B always equals B @ A.", "false"),
        ],
    }
    hints_by_difficulty = {
        "easy": "Think about matrix properties and operations",
        "medium": "Consider matrix operation requirements and properties",
        "hard": "Advanced matrix operations involve understanding linear algebra concepts",
    }
    question, answer, hint = pick_true_false_statement(
        difficulty, statements_by_difficulty, hints_by_difficulty, used_questions=used_questions
    )
    return {"type": "true_false", "question": question, "answer": answer, "hint": hint}


def validate_code_answer(user_input, correct_answer):
    """Validate user's code answer using shared matrix profile."""
    return shared_validate_code_answer(user_input, correct_answer, profile="matrix")


def show_hint(challenge):
    """Display a hint for the current challenge."""
    print(f"Hint: {challenge['hint']}")


def play_game():
    """Run a single game session."""

    challenge_functions = [
        generate_create_matrix_challenge,
        generate_matrix_math_challenge,
        generate_transpose_challenge,
        generate_matrix_shape_challenge,
        generate_reshape_matrix_challenge,
        generate_matrix_properties_challenge,
    ]

    def build_sequence(_difficulty, code_count, tf_count, used_questions):
        challenge_sequence = [random.choice(challenge_functions) for _ in range(code_count)]
        for _ in range(tf_count):
            challenge_sequence.append(
                lambda d, u=used_questions: generate_true_false_challenge(d, used_questions=u)
            )
        random.shuffle(challenge_sequence)
        return challenge_sequence

    run_game_session(
        game_name="Matrix Challenge",
        subtitle="Master NumPy matrix operations!",
        perfect_message="Perfect score! You're a matrix master! 🎉",
        thank_you_message="Thank you for playing Matrix Challenge!",
        code_validator=validate_code_answer,
        sequence_builder=build_sequence,
        show_hint=show_hint,
    )


def main():
    """Main game loop with play-again prompt."""
    run_with_replay(play_game)


if __name__ == "__main__":
    main()