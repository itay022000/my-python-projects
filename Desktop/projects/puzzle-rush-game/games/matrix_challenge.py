import numpy as np
import random
from exercise_session import run_standard_game
from session_common import EXERCISE_BACKGROUNDS, build_teach_body_lines, pick_true_false_statement
from hints import HINT_021, HINT_022, HINT_023, HINT_024, HINT_025, HINT_026, HINT_027, HINT_028, HINT_029, HINT_030
"""
Matrix Challenge - Solve matrix operations and transformations

This game challenges you to:
- Create 2D arrays (matrices)
- Perform matrix operations (addition, multiplication)
- Understand matrix properties (transpose, shape)
- Reshape matrices
- Work with matrix math
"""


def generate_create_matrix_challenge():
    """Generate challenge to create a matrix"""
    question_type = random.choice(['zeros', 'ones', 'identity', 'random', 'full'])
    if question_type == 'zeros':
        rows = random.randint(4, 8)
        cols = random.randint(4, 8)
        dtype = random.choice(['int', 'float'])
        question = f'Write the code to create a {rows}x{cols} matrix of zeros with dtype {dtype}'
        answer = f'np.zeros(({rows}, {cols}), dtype=np.{dtype})'
    elif question_type == 'ones':
        rows = random.randint(4, 8)
        cols = random.randint(4, 8)
        dtype = random.choice(['int', 'float'])
        question = f'Write the code to create a {rows}x{cols} matrix of ones with dtype {dtype}'
        answer = f'np.ones(({rows}, {cols}), dtype=np.{dtype})'
    elif question_type == 'identity':
        size = random.randint(4, 8)
        question = f'Write the code to create a {size}x{size} identity matrix'
        answer = f'np.eye({size})'
    elif question_type == 'random':
        rows = random.randint(4, 8)
        cols = random.randint(4, 8)
        low = random.randint(-10, 0)
        high = random.randint(20, 50)
        question = f'Write the code to create a {rows}x{cols} matrix with random integers from {low} to {high - 1}'
        answer = f'np.random.randint({low}, {high}, size=({rows}, {cols}))'
    else:
        rows = random.randint(4, 8)
        cols = random.randint(4, 8)
        value = random.randint(1, 20)
        dtype = random.choice(['int', 'float'])
        question = f'Write the code to create a {rows}x{cols} matrix filled with {value} (dtype {dtype})'
        answer = f'np.full(({rows}, {cols}), {value}, dtype=np.{dtype})'
    creation_hint = HINT_021
    hint = creation_hint
    return {'type': 'create_matrix', 'question': question, 'answer': answer, 'hint': hint}

def generate_matrix_math_challenge():
    """Generate challenge for matrix arithmetic"""
    question_type = random.choice(['add', 'subtract', 'multiply', 'dot', 'scalar'])
    _element_wise_hint = HINT_022
    if question_type == 'add':
        rows = random.randint(4, 6)
        cols = random.randint(4, 6)
        A = np.random.randint(0, 50, size=(rows, cols))
        B = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrices A and B, write the code to add them'
        answer = 'np.add(A, B)'
        hint = _element_wise_hint
    elif question_type == 'subtract':
        rows = random.randint(4, 6)
        cols = random.randint(4, 6)
        A = np.random.randint(20, 50, size=(rows, cols))
        B = np.random.randint(0, 20, size=(rows, cols))
        question = f'Given the matrices A and B, write the code to subtract B from A'
        answer = 'np.subtract(A, B)'
        hint = _element_wise_hint
    elif question_type == 'multiply':
        rows = random.randint(4, 6)
        cols = random.randint(4, 6)
        A = np.random.randint(0, 50, size=(rows, cols))
        B = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrices A and B, write the code to multiply them element-wise'
        answer = 'np.multiply(A, B)'
        hint = _element_wise_hint
    elif question_type == 'dot':
        rows1 = random.randint(4, 6)
        cols1 = random.randint(4, 6)
        rows2 = cols1
        cols2 = random.randint(4, 6)
        A = np.random.randint(0, 50, size=(rows1, cols1))
        B = np.random.randint(0, 50, size=(rows2, cols2))
        question = f'Given the matrices A and B, write the code to compute matrix multiplication'
        answer = 'np.dot(A, B)'
        hint = HINT_030
    else:
        rows = random.randint(4, 6)
        cols = random.randint(4, 6)
        matrix = np.random.randint(0, 50, size=(rows, cols))
        scalar = random.randint(2, 20)
        question = f'Given the matrix M, write the code to multiply it by scalar {scalar}'
        answer = f'np.multiply(M, {scalar})'
        hint = _element_wise_hint
    return {'type': 'matrix_math', 'question': question, 'answer': answer, 'hint': hint}

def generate_transpose_challenge():
    """Generate challenge about matrix transpose"""
    question_type = random.choice(['transpose', 'T', 'property'])
    _transpose_code_hint = HINT_023
    if question_type == 'transpose':
        rows = random.randint(4, 7)
        cols = random.randint(4, 7)
        matrix = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrix M, write the code to get its transpose'
        answer = 'np.transpose(M)'
        hint = _transpose_code_hint
    elif question_type == 'T':
        rows = random.randint(4, 7)
        cols = random.randint(4, 7)
        matrix = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrix M, write the code to transpose it'
        answer = 'M.T'
        hint = _transpose_code_hint
    else:
        rows = random.randint(4, 8)
        cols = random.randint(4, 8)
        question = f'If a matrix has shape ({rows}, {cols}), what is the shape of its transpose?\nWrite as a tuple'
        answer = f'({cols}, {rows})'
        hint = HINT_028
    return {'type': 'transpose', 'question': question, 'answer': answer, 'hint': hint}

def generate_matrix_shape_challenge():
    """Generate challenge about matrix shape"""
    question_type = random.choice(['shape', 'size', 'ndim'])
    if question_type == 'shape':
        rows = random.randint(4, 7)
        cols = random.randint(4, 7)
        matrix = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrix M, write the code to get its shape'
        answer = 'M.shape'
    elif question_type == 'size':
        rows = random.randint(4, 7)
        cols = random.randint(4, 7)
        matrix = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrix M, write the code to get the total number of elements'
        answer = 'M.size'
    else:
        matrix = np.random.randint(0, 50, size=(random.randint(4, 7), random.randint(4, 7)))
        question = f'Given the matrix M, write the code to get the number of dimensions'
        answer = 'M.ndim'
    hint = HINT_024
    return {'type': 'matrix_shape', 'question': question, 'answer': answer, 'hint': hint}

def generate_reshape_matrix_challenge():
    """Generate challenge to reshape a matrix"""
    question_type = random.choice(['reshape', 'flatten', 'ravel'])
    _flatten_hint = HINT_025
    if question_type == 'reshape':
        rows = random.randint(4, 6)
        cols = random.randint(4, 6)
        total = rows * cols
        new_rows = random.choice([i for i in range(2, total // 2 + 1) if total % i == 0])
        new_cols = total // new_rows
        matrix = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrix M, write the code to reshape it to ({new_rows}, {new_cols})'
        answer = f'M.reshape(({new_rows}, {new_cols}))'
        hint = HINT_026
    elif question_type == 'flatten':
        rows = random.randint(4, 6)
        cols = random.randint(4, 6)
        matrix = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrix M, write the code to flatten the matrix into one dimension'
        answer = 'M.flatten()'
        hint = _flatten_hint
    else:
        rows = random.randint(4, 6)
        cols = random.randint(4, 6)
        matrix = np.random.randint(0, 50, size=(rows, cols))
        question = f'Given the matrix M, write the code to ravel the matrix into one dimension'
        answer = 'M.ravel()'
        hint = _flatten_hint
    return {'type': 'reshape_matrix', 'question': question, 'answer': answer, 'hint': hint}

def generate_matrix_properties_challenge():
    """Generate challenge about matrix properties"""
    question_type = random.choice(['symmetric', 'identity', 'square', 'diagonal'])
    if question_type == 'symmetric':
        size = random.randint(4, 6)
        matrix = np.random.randint(0, 50, size=(size, size))
        matrix = (matrix + matrix.T) // 2
        question = f"Given the matrix M, write the code to check if it's symmetric"
        answer = 'np.array_equal(M, M.T)'
        hint = HINT_027
    elif question_type == 'identity':
        size = random.randint(4, 6)
        question = f'Write the code to create a {size}x{size} identity matrix'
        answer = f'np.eye({size})'
        hint = HINT_021
    elif question_type == 'square':
        size = random.randint(4, 6)
        matrix = np.random.randint(0, 50, size=(size, size))
        question = f"Given the matrix M, write the code to check if it's square"
        answer = 'M.shape[0] == M.shape[1]'
        hint = HINT_027
    else:
        size = random.randint(4, 6)
        matrix = np.eye(size) * np.random.randint(1, 50, size=size)
        question = f'Given the matrix M, write the code to extract the diagonal elements'
        answer = 'np.diag(M)'
        hint = HINT_029
    return {'type': 'matrix_properties', 'question': question, 'answer': answer, 'hint': hint}

def generate_true_false_challenge(*, used_questions=None):
    """Generate true/false questions about matrix operations."""
    statements = [
        ('True or False: np.full((3, 4), 5) creates a 3x4 matrix filled with 5s.', 'True'),
        ('True or False: M.ndim returns the number of dimensions (2 for a matrix).', 'True'),
        ('True or False: You can use -1 in reshape to automatically calculate one dimension.', 'True'),
        ('True or False: np.array_equal(M, M.T) checks if a matrix is symmetric.', 'True'),
        ('True or False: Matrix multiplication is not commutative (A @ B ≠ B @ A in general).', 'True'),
        ('True or False: Element-wise multiplication with * is different from matrix multiplication with @.', 'True'),
        ('True or False: NumPy can broadcast a scalar to multiply with a matrix element-wise.', 'True'),
        ('True or False: np.dot(A, B) performs element-wise multiplication.', 'False'),
        ('True or False: Transposing twice returns the inverse of the original matrix.', 'False'),
        ('True or False: Multiplying any matrix by an identity matrix of compatible size always returns the identity matrix.', 'False'),
        ('True or False: M.flatten() always returns a view sharing memory with the original matrix.', 'False'),
        ('True or False: For any two square matrices A and B of the same shape, A @ B always equals B @ A.', 'False'),
    ]
    question, answer = pick_true_false_statement(statements, used_questions=used_questions)
    return {'type': 'true_false', 'question': question, 'answer': answer, 'hint': ''}

def play_game():
    """Run a single game session."""
    run_standard_game(teach_title='Matrix Challenge - Matrix Exercise', teach_body_lines=build_teach_body_lines('You will get 20 single-line questions (15 code questions followed by 5 True/False questions).'), validator_profile='matrix', code_generators=[generate_create_matrix_challenge, generate_matrix_math_challenge, generate_transpose_challenge, generate_matrix_shape_challenge, generate_reshape_matrix_challenge, generate_matrix_properties_challenge], true_false_factory=generate_true_false_challenge, background=EXERCISE_BACKGROUNDS["matrix_challenge"])

def main():
    """Legacy entry — redirects learners to main.py (does not start a round)."""
    print('Use python3 main.py for the full menu.')
if __name__ == '__main__':
    main()
