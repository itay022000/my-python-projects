import numpy as np
import random
from exercise_session import run_standard_game
from session_common import EXERCISE_BACKGROUNDS, build_teach_body_lines, pick_true_false_statement
from hints import HINT_004, HINT_022, HINT_031, HINT_032, HINT_033, HINT_034, HINT_035, HINT_036, HINT_037, HINT_038, HINT_039, HINT_040, HINT_041, HINT_042, HINT_043, HINT_044, HINT_045, HINT_046, HINT_047
"""
Ufunc Arena - Master NumPy Universal Functions

This game challenges you to:
- Use arithmetic operations (add, subtract, multiply, divide)
- Apply rounding functions (round, floor, ceil)
- Work with logarithms (log, log10, log2)
- Use aggregations (sum, product, mean)
- Calculate differences
- Find LCM and GCD
- Perform set operations
"""


def generate_arithmetic_challenge():
    """Generate challenge for arithmetic operations"""
    question_type = random.choice(['add', 'subtract', 'multiply', 'divide', 'power', 'mod'])
    _arithmetic_hint = HINT_022
    if question_type == 'add':
        array1 = np.random.randint(0, 20, size=(random.randint(3, 5), random.randint(3, 5)))
        array2 = np.random.randint(0, 20, size=array1.shape)
        question = f'Given the arrays a and b, write the code to add them element-wise'
        answer = 'np.add(a, b)'
    elif question_type == 'subtract':
        array1 = np.random.randint(10, 30, size=(random.randint(3, 5), random.randint(3, 5)))
        array2 = np.random.randint(0, 10, size=array1.shape)
        question = f'Given the arrays a and b, write the code to subtract b from a'
        answer = 'np.subtract(a, b)'
    elif question_type == 'multiply':
        array1 = np.random.randint(1, 15, size=(random.randint(3, 5), random.randint(3, 5)))
        array2 = np.random.randint(1, 15, size=array1.shape)
        question = f'Given the arrays a and b, write the code to multiply them element-wise'
        answer = 'np.multiply(a, b)'
    elif question_type == 'divide':
        array1 = np.random.randint(20, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        array2 = np.random.randint(2, 8, size=array1.shape)
        question = f'Given the arrays a and b, write the code to divide a by b'
        answer = 'np.divide(a, b)'
    elif question_type == 'power':
        base = np.random.randint(2, 6, size=(random.randint(3, 4), random.randint(3, 4)))
        exp = random.randint(2, 5)
        question = f'Given the array a, write the code to raise each element to the power of {exp}'
        answer = f'np.power(a, {exp})'
    else:
        array1 = np.random.randint(20, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        array2 = np.random.randint(3, 10, size=array1.shape)
        question = f'Given the arrays a and b, write the code to compute element-wise modulo'
        answer = 'np.mod(a, b)'
    hint = _arithmetic_hint
    return {'type': 'arithmetic', 'question': question, 'answer': answer, 'hint': hint}

def generate_rounding_challenge():
    """Generate challenge for rounding operations"""
    question_type = random.choice(['round', 'floor', 'ceil', 'trunc'])
    if question_type == 'round':
        array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
        decimals = random.randint(0, 3)
        question = f'Given the array a, write the code to round each element to {decimals} decimal places'
        answer = f'np.round(a, {decimals})'
    elif question_type == 'floor':
        array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to round each element down to the nearest integer'
        answer = 'np.floor(a)'
    elif question_type == 'ceil':
        array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to round each element up to the nearest integer'
        answer = 'np.ceil(a)'
    else:
        array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to truncate each element (remove decimal part)'
        answer = 'np.trunc(a)'
    hint = HINT_031
    return {'type': 'rounding', 'question': question, 'answer': answer, 'hint': hint}

def generate_logarithm_challenge():
    """Generate challenge for logarithm operations"""
    question_type = random.choice(['log', 'log10', 'log2', 'exp'])
    if question_type == 'log':
        array = np.random.randint(1, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to compute the natural logarithm of each element'
        answer = 'np.log(a)'
    elif question_type == 'log10':
        array = np.random.randint(1, 1000, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to compute the base-10 logarithm of each element'
        answer = 'np.log10(a)'
    elif question_type == 'log2':
        array = np.random.randint(1, 64, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to compute the base-2 logarithm of each element'
        answer = 'np.log2(a)'
    else:
        array = np.random.uniform(0.1, 4.0, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to compute e raised to the power of each element'
        answer = 'np.exp(a)'
    hint = HINT_032
    return {'type': 'logarithm', 'question': question, 'answer': answer, 'hint': hint}

def generate_summation_challenge():
    """Generate challenge for summation"""
    question_type = random.choice(['sum', 'cumsum', 'axis'])
    if question_type == 'sum':
        array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
        question = f'Given the array a, write the code to compute the sum of all elements'
        answer = 'np.sum(a)'
        hint = HINT_035
    elif question_type == 'cumsum':
        array = np.random.randint(1, 50, size=random.randint(10, 15))
        question = f'Given the array a, write the code to compute the cumulative sum'
        answer = 'np.cumsum(a)'
        hint = HINT_039
    else:
        array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
        axis = random.choice([0, 1])
        question = f'Given the array a, write the code to sum along axis {axis}'
        answer = f'np.sum(a, axis={axis})'
        hint = HINT_004
    return {'type': 'summation', 'question': question, 'answer': answer, 'hint': hint}

def generate_product_challenge():
    """Generate challenge for product"""
    question_type = random.choice(['prod', 'cumprod', 'axis'])
    if question_type == 'prod':
        array = np.random.randint(1, 20, size=(random.randint(4, 5), random.randint(4, 5)))
        question = f'Given the array a, write the code to compute the product of all elements'
        answer = 'np.prod(a)'
        hint = HINT_036
    elif question_type == 'cumprod':
        array = np.random.randint(1, 20, size=random.randint(8, 12))
        question = f'Given the array a, write the code to compute the cumulative product'
        answer = 'np.cumprod(a)'
        hint = HINT_040
    else:
        array = np.random.randint(1, 20, size=(random.randint(4, 6), random.randint(4, 6)))
        axis = random.choice([0, 1])
        question = f'Given the array a, write the code to compute product along axis {axis}'
        answer = f'np.prod(a, axis={axis})'
        hint = HINT_041
    return {'type': 'product', 'question': question, 'answer': answer, 'hint': hint}

def generate_difference_challenge():
    """Generate challenge for differences"""
    question_type = random.choice(['diff', 'gradient', 'ediff1d'])
    if question_type == 'diff':
        array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
        axis = random.choice([0, 1])
        question = f'Given the array a, write the code to compute differences along axis {axis}'
        answer = f'np.diff(a, axis={axis})'
        hint = HINT_037
    elif question_type == 'gradient':
        array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
        question = f'Given the array a, write the code to compute the gradient'
        answer = 'np.gradient(a)'
        hint = HINT_042
    else:
        array = np.random.randint(1, 50, size=random.randint(10, 15))
        question = f'Given the array a, write the code to compute element-wise differences'
        answer = 'np.ediff1d(a)'
        hint = HINT_043
    return {'type': 'difference', 'question': question, 'answer': answer, 'hint': hint}

def generate_lcm_gcd_challenge():
    """Generate challenge for LCM and GCD"""
    question_type = random.choice(['gcd', 'lcm', 'array_gcd', 'array_lcm'])
    _scalar_reduce_hint = HINT_033
    _array_reduce_hint = HINT_034
    if question_type == 'gcd':
        a = random.randint(50, 100)
        b = random.randint(50, 100)
        c = random.randint(50, 100)
        question = f'Write the code to find the GCD of {a}, {b}, and {c} using NumPy'
        answer = f'np.gcd.reduce([{a}, {b}, {c}])'
        hint = _scalar_reduce_hint
    elif question_type == 'lcm':
        a = random.randint(20, 60)
        b = random.randint(20, 60)
        c = random.randint(20, 60)
        question = f'Write the code to find the LCM of {a}, {b}, and {c} using NumPy'
        answer = f'np.lcm.reduce([{a}, {b}, {c}])'
        hint = _scalar_reduce_hint
    elif question_type == 'array_gcd':
        array = np.random.randint(50, 100, size=random.randint(8, 12))
        question = f'Given the array a, write the code to find GCD of all elements'
        answer = 'np.gcd.reduce(a)'
        hint = _array_reduce_hint
    else:
        array = np.random.randint(20, 60, size=random.randint(8, 12))
        question = f'Given the array a, write the code to find LCM of all elements'
        answer = 'np.lcm.reduce(a)'
        hint = _array_reduce_hint
    return {'type': 'lcm_gcd', 'question': question, 'answer': answer, 'hint': hint}

def generate_set_operations_challenge():
    """Generate challenge for set operations"""
    question_type = random.choice(['unique', 'intersect', 'union', 'setdiff', 'setxor'])
    if question_type == 'unique':
        array = np.random.randint(1, 50, size=random.randint(15, 25))
        question = f'Given the array a, write the code to get unique values'
        answer = 'np.unique(a)'
        hint = HINT_038
    elif question_type == 'intersect':
        array1 = np.random.randint(1, 50, size=random.randint(12, 18))
        array2 = np.random.randint(1, 50, size=random.randint(12, 18))
        question = f'Given the arrays a and b, write the code to find common elements'
        answer = 'np.intersect1d(a, b)'
        hint = HINT_044
    elif question_type == 'union':
        array1 = np.random.randint(1, 50, size=random.randint(12, 18))
        array2 = np.random.randint(1, 50, size=random.randint(12, 18))
        question = f'Given the arrays a and b, write the code to find all unique elements from both arrays'
        answer = 'np.union1d(a, b)'
        hint = HINT_045
    elif question_type == 'setdiff':
        array1 = np.random.randint(1, 50, size=random.randint(12, 18))
        array2 = np.random.randint(1, 50, size=random.randint(12, 18))
        question = f'Given the arrays a and b, write the code to find elements in a but not in b'
        answer = 'np.setdiff1d(a, b)'
        hint = HINT_046
    else:
        array1 = np.random.randint(1, 50, size=random.randint(12, 18))
        array2 = np.random.randint(1, 50, size=random.randint(12, 18))
        question = f'Given the arrays a and b, write the code to find elements in either array but not both'
        answer = 'np.setxor1d(a, b)'
        hint = HINT_047
    return {'type': 'set_operations', 'question': question, 'answer': answer, 'hint': hint}

def generate_true_false_challenge(*, used_questions=None):
    """Generate true/false questions about ufunc operations."""
    statements = [
        ('True or False: np.divide() can handle broadcasting when array shapes are compatible.', 'True'),
        ('True or False: np.trunc() and np.floor() always return the same result for positive numbers.', 'True'),
        ('True or False: np.cumsum(a) returns the cumulative sum as a new array.', 'True'),
        ('True or False: np.cumprod(a) computes the cumulative product.', 'True'),
        ('True or False: np.lcm.reduce([4, 6, 8]) finds the LCM of all three numbers.', 'True'),
        ('True or False: Ufuncs automatically broadcast arrays with compatible shapes.', 'True'),
        ('True or False: Aggregation functions like sum() and prod() can operate along specific axes.', 'True'),
        ('True or False: np.exp(np.log(x)) returns x for every x, including non-positive x.', 'False'),
        ('True or False: np.diff(a, n=2) computes first-order differences.', 'False'),
        ('True or False: np.setdiff1d(a, b) returns elements in b but not in a.', 'False'),
        ('True or False: np.prod on an empty array returns 0.', 'False'),
        ('True or False: np.trunc(x) and np.floor(x) always return the same value for every x.', 'False'),
    ]
    question, answer = pick_true_false_statement(statements, used_questions=used_questions)
    return {'type': 'true_false', 'question': question, 'answer': answer, 'hint': ''}

def play_game():
    """Run a single game session."""
    run_standard_game(teach_title='Ufunc Arena - Ufunc Exercise', teach_body_lines=build_teach_body_lines('You will get 20 single-line questions (15 code questions followed by 5 True/False questions).'), validator_profile='default', code_generators=[generate_arithmetic_challenge, generate_rounding_challenge, generate_logarithm_challenge, generate_summation_challenge, generate_product_challenge, generate_difference_challenge, generate_lcm_gcd_challenge, generate_set_operations_challenge], true_false_factory=generate_true_false_challenge, background=EXERCISE_BACKGROUNDS["ufunc_arena"])

def main():
    """Legacy entry — redirects learners to main.py (does not start a round)."""
    print('Use python3 main.py for the full menu.')
if __name__ == '__main__':
    main()
