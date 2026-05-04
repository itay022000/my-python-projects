import numpy as np
import random

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
            question = f"Given: matrix = \n{matrix}\nWrite the code to transpose it using the .T attribute"
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
            question = f"Given: matrix = \n{matrix}\nWrite the code to transpose it using the .T attribute"
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
            question = f"Given: matrix = \n{matrix}\nWrite the code to transpose it using the .T attribute"
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


def generate_true_false_challenge(difficulty="easy"):
    """Generate true/false questions about matrix operations"""
    question_type = random.choice([
        "creation", "math", "transpose", "shape", "reshape",
        "properties", "dot", "elementwise", "broadcasting", "identity"
    ])
    
    if difficulty == "easy":
        if question_type == "creation":
            question = "True or False: np.zeros((3, 4)) creates a 3x4 matrix filled with zeros."
            answer = "true"
        elif question_type == "math":
            question = "True or False: Matrix addition requires both matrices to have the same shape."
            answer = "true"
        elif question_type == "transpose":
            question = "True or False: Transposing a (3, 4) matrix gives a (4, 3) matrix."
            answer = "true"
        elif question_type == "shape":
            question = "True or False: matrix.shape returns a tuple (rows, cols)."
            answer = "true"
        else:  # reshape
            question = "True or False: You can reshape a (2, 6) matrix to (3, 4) because both have 12 elements."
            answer = "true"
        hint = "Think about matrix properties and operations"
    elif difficulty == "medium":
        if question_type == "creation":
            question = "True or False: np.eye(5) creates a 5x5 identity matrix."
            answer = "true"
        elif question_type == "math":
            question = "True or False: np.multiply(a, b) performs element-wise multiplication, not matrix multiplication."
            answer = "true"
        elif question_type == "transpose":
            question = "True or False: matrix.T and np.transpose(matrix) are equivalent for 2D arrays."
            answer = "true"
        elif question_type == "shape":
            question = "True or False: matrix.size returns the total number of elements (rows * cols)."
            answer = "true"
        elif question_type == "reshape":
            question = "True or False: reshape() requires the total number of elements to remain the same."
            answer = "true"
        elif question_type == "properties":
            question = "True or False: A symmetric matrix equals its transpose."
            answer = "true"
        elif question_type == "dot":
            question = "True or False: For np.dot(a, b) to work, the number of columns in a must equal the number of rows in b."
            answer = "true"
        elif question_type == "elementwise":
            question = "True or False: Element-wise operations require matrices to have the same shape."
            answer = "true"
        else:  # identity
            question = "True or False: An identity matrix has 1s on the diagonal and 0s elsewhere."
            answer = "true"
        hint = "Consider matrix operation requirements and properties"
    else:  # hard
        if question_type == "creation":
            question = "True or False: np.full((3, 4), 5) creates a 3x4 matrix filled with 5s."
            answer = "true"
        elif question_type == "math":
            question = "True or False: np.dot(a, b) performs matrix multiplication (not element-wise)."
            answer = "true"
        elif question_type == "transpose":
            question = "True or False: Transposing twice returns the original matrix."
            answer = "true"
        elif question_type == "shape":
            question = "True or False: matrix.ndim returns the number of dimensions (2 for a matrix)."
            answer = "true"
        elif question_type == "reshape":
            question = "True or False: You can use -1 in reshape to automatically calculate one dimension."
            answer = "true"
        elif question_type == "properties":
            question = "True or False: np.array_equal(matrix, matrix.T) checks if a matrix is symmetric."
            answer = "true"
        elif question_type == "dot":
            question = "True or False: Matrix multiplication is not commutative (A @ B ≠ B @ A in general)."
            answer = "true"
        elif question_type == "elementwise":
            question = "True or False: Element-wise multiplication with * is different from matrix multiplication with @."
            answer = "true"
        elif question_type == "broadcasting":
            question = "True or False: NumPy can broadcast a scalar to multiply with a matrix element-wise."
            answer = "true"
        else:  # identity
            question = "True or False: Multiplying any matrix by an identity matrix of compatible size returns the original matrix."
            answer = "true"
        hint = "Advanced matrix operations involve understanding linear algebra concepts"
    
    return {"type": "true_false", "question": question, "answer": answer, "hint": hint}


def validate_code_answer(user_input, correct_answer):
    """
    Validate user's code answer.
    Normalizes whitespace and handles variations in code formatting.
    """
    def normalize_code(code):
        # Remove all whitespace
        code = ''.join(code.split())
        # Convert to lowercase for case-insensitive comparison
        return code.lower()
    
    user_normalized = normalize_code(user_input)
    correct_normalized = normalize_code(correct_answer)
    
    # Handle tuple answers (for shape questions)
    if correct_normalized.startswith('(') and correct_normalized.endswith(')'):
        # Remove parentheses and normalize spaces
        correct_clean = correct_normalized.strip('()').replace(' ', '')
        user_clean = user_normalized.strip('()').replace(' ', '')
        return user_clean == correct_clean
    
    # Handle transpose equivalence: matrix.T and np.transpose(matrix) are equivalent
    # Check if correct answer is a transpose operation
    correct_is_transpose_t = correct_normalized == "matrix.t" or correct_normalized.endswith(".t")
    correct_is_transpose_func = "nptranspose(matrix)" in correct_normalized or "transpose(matrix)" in correct_normalized
    
    # Check if user answer is a transpose operation
    user_is_transpose_t = user_normalized == "matrix.t" or user_normalized.endswith(".t")
    user_is_transpose_func = "nptranspose(matrix)" in user_normalized or "transpose(matrix)" in user_normalized
    
    # If both are transpose operations (either form), accept it
    if (correct_is_transpose_t or correct_is_transpose_func) and (user_is_transpose_t or user_is_transpose_func):
        return True
    
    return user_normalized == correct_normalized


def show_hint(challenge):
    """Display a hint for the current challenge."""
    print(f"Hint: {challenge['hint']}")


def play_game():
    """
    Run a single game session.
    """
    print("Welcome to Matrix Challenge!")
    print("Master NumPy matrix operations!\n")
    
    # Difficulty selection
    while True:
        difficulty = input("Select difficulty (easy/medium/hard or 1/2/3): ").strip().lower()
        # Map numeric shortcuts to difficulty levels
        if difficulty == "1":
            difficulty = "easy"
        elif difficulty == "2":
            difficulty = "medium"
        elif difficulty == "3":
            difficulty = "hard"
        if difficulty in ["easy", "medium", "hard"]:
            break
        print("Invalid choice. Please enter 'easy', 'medium', 'hard', or '1', '2', '3'.")
    
    print(f"\nYou selected {difficulty.upper()} difficulty. Good luck!")
    print("(Tip: Type 'exit' at any time to quit the current round)\n")
    
    # Set number of challenges based on difficulty
    if difficulty == "easy":
        total_challenges = 6  # 5 code + 1 T/F
    elif difficulty == "medium":
        total_challenges = 13  # 10 code + 3 T/F
    else:  # hard
        total_challenges = 20  # 15 code + 5 T/F
    
    # Initialize score tracking
    score = 0
    
    # Challenge functions
    challenge_functions = [
        generate_create_matrix_challenge,
        generate_matrix_math_challenge,
        generate_transpose_challenge,
        generate_matrix_shape_challenge,
        generate_reshape_matrix_challenge,
        generate_matrix_properties_challenge
    ]
    
    # Create challenge sequence with diversity
    challenge_sequence = []
    for _ in range(total_challenges):
        challenge_sequence.append(random.choice(challenge_functions))
    
    # Shuffle to randomize order
    random.shuffle(challenge_sequence)
    
    # Game loop
    for i in range(total_challenges):
        print(f"--- Challenge {i + 1} of {total_challenges} ---")
        
        # Get challenge function from sequence
        challenge_func = challenge_sequence[i]
        challenge = challenge_func(difficulty)
        
        # Display question
        print(f"\n{challenge['question']}\n")
        
        # Get user input - check if it's a T/F question
        if challenge['type'] == 'true_false':
            user_answer = input("Your answer (true/false or t/f): ").strip().lower()
            # Check for exit command
            if user_answer == 'exit':
                print("\nRound ended. Returning to menu...")
                return
            # Normalize T/F answers
            if user_answer in ['t', 'true']:
                user_answer = 'true'
            elif user_answer in ['f', 'false']:
                user_answer = 'false'
            is_correct = user_answer == challenge['answer']
        else:
            user_answer = input("Your answer (write the code): ").strip()
            # Check for exit command
            if user_answer.lower() == 'exit':
                print("\nRound ended. Returning to menu...")
                return
            # Normalize spaces before validation
            is_correct = validate_code_answer(user_answer, challenge['answer'])
        
        # Update score and show feedback
        if is_correct:
            print("✓ Correct! Well done!")
            score += 1
        else:
            print(f"✗ Incorrect. The correct answer is: {challenge['answer']}")
            show_hint(challenge)
        
        print(f"Current score: {score}/{i + 1}\n")
    
    # Final statistics
    percentage = (score / total_challenges) * 100
    print("=" * 50)
    print(f"Final Score: {score} out of {total_challenges}")
    print(f"Percentage: {percentage:.1f}%")
    
    if percentage == 100:
        print("Perfect score! You're a matrix master! 🎉")
    elif percentage >= 80:
        print("Excellent work! You're getting really good! 🌟")
    elif percentage >= 60:
        print("Good job! Keep practicing! 👍")
    else:
        print("Keep practicing! You'll get better! 💪")
    
    print("\nThank you for playing Matrix Challenge!")


def main():
    """
    Main game loop with play again option.
    """
    while True:
        play_game()
        
        # Ask if user wants to play again
        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").strip().lower()
            if play_again in ["yes", "y", "no", "n"]:
                break
            print("Invalid choice. Please enter 'yes' or 'no'.")
        
        if play_again in ["no", "n"]:
            print("\nWe'll talk later! 👋")
            break
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()