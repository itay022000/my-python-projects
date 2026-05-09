import numpy as np
import random
from code_validators import validate_code_answer as shared_validate_code_answer
from engine import run_game_session, run_with_replay
from game_common import pick_true_false_statement

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


def generate_arithmetic_challenge(difficulty="easy"):
    """Generate challenge for arithmetic operations"""
    question_type = random.choice(["add", "subtract", "multiply", "divide", "power", "mod"])
    
    if difficulty == "easy":
        if question_type == "add":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            question = f"Write the code to add {a} and {b} using NumPy"
            answer = f"np.add({a}, {b})"
        elif question_type == "subtract":
            a = random.randint(5, 15)
            b = random.randint(1, 5)
            question = f"Write the code to subtract {b} from {a} using NumPy"
            answer = f"np.subtract({a}, {b})"
        elif question_type == "multiply":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            question = f"Write the code to multiply {a} and {b} using NumPy"
            answer = f"np.multiply({a}, {b})"
        elif question_type == "divide":
            a = random.randint(10, 20)
            b = random.randint(2, 5)
            question = f"Write the code to divide {a} by {b} using NumPy"
            answer = f"np.divide({a}, {b})"
        elif question_type == "power":
            base = random.randint(2, 5)
            exp = random.randint(2, 4)
            question = f"Write the code to raise {base} to the power of {exp} using NumPy"
            answer = f"np.power({base}, {exp})"
        else:  # mod
            a = random.randint(10, 20)
            b = random.randint(3, 7)
            question = f"Write the code to compute {a} modulo {b} using NumPy"
            answer = f"np.mod({a}, {b})"
        hint = "NumPy has arithmetic functions like add, subtract, multiply, divide"
    elif difficulty == "medium":
        if question_type == "add":
            array1 = np.random.randint(0, 10, size=random.randint(5, 8))
            array2 = np.random.randint(0, 10, size=len(array1))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to add them element-wise"
            answer = "np.add(array1, array2)"
        elif question_type == "subtract":
            array1 = np.random.randint(5, 15, size=random.randint(5, 8))
            array2 = np.random.randint(0, 5, size=len(array1))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to subtract array2 from array1"
            answer = "np.subtract(array1, array2)"
        elif question_type == "multiply":
            array1 = np.random.randint(1, 10, size=random.randint(5, 8))
            array2 = np.random.randint(1, 10, size=len(array1))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to multiply them element-wise"
            answer = "np.multiply(array1, array2)"
        elif question_type == "divide":
            array1 = np.random.randint(10, 30, size=random.randint(5, 8))
            array2 = np.random.randint(2, 6, size=len(array1))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to divide array1 by array2"
            answer = "np.divide(array1, array2)"
        elif question_type == "power":
            base = np.random.randint(2, 5, size=random.randint(4, 7))
            exp = random.randint(2, 4)
            question = f"Given: base = {base}\nWrite the code to raise each element to the power of {exp}"
            answer = f"np.power(base, {exp})"
        else:  # mod
            array1 = np.random.randint(10, 30, size=random.randint(5, 8))
            array2 = np.random.randint(3, 8, size=len(array1))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to compute element-wise modulo"
            answer = "np.mod(array1, array2)"
        hint = "NumPy arithmetic functions work element-wise on arrays"
    else:  # hard
        if question_type == "add":
            array1 = np.random.randint(0, 20, size=(random.randint(3, 5), random.randint(3, 5)))
            array2 = np.random.randint(0, 20, size=array1.shape)
            question = f"Given: array1 = \n{array1}, array2 = \n{array2}\nWrite the code to add them element-wise"
            answer = "np.add(array1, array2)"
        elif question_type == "subtract":
            array1 = np.random.randint(10, 30, size=(random.randint(3, 5), random.randint(3, 5)))
            array2 = np.random.randint(0, 10, size=array1.shape)
            question = f"Given: array1 = \n{array1}, array2 = \n{array2}\nWrite the code to subtract array2 from array1"
            answer = "np.subtract(array1, array2)"
        elif question_type == "multiply":
            array1 = np.random.randint(1, 15, size=(random.randint(3, 5), random.randint(3, 5)))
            array2 = np.random.randint(1, 15, size=array1.shape)
            question = f"Given: array1 = \n{array1}, array2 = \n{array2}\nWrite the code to multiply them element-wise"
            answer = "np.multiply(array1, array2)"
        elif question_type == "divide":
            array1 = np.random.randint(20, 50, size=(random.randint(3, 5), random.randint(3, 5)))
            array2 = np.random.randint(2, 8, size=array1.shape)
            question = f"Given: array1 = \n{array1}, array2 = \n{array2}\nWrite the code to divide array1 by array2"
            answer = "np.divide(array1, array2)"
        elif question_type == "power":
            base = np.random.randint(2, 6, size=(random.randint(3, 4), random.randint(3, 4)))
            exp = random.randint(2, 5)
            question = f"Given: base = \n{base}\nWrite the code to raise each element to the power of {exp}"
            answer = f"np.power(base, {exp})"
        else:  # mod
            array1 = np.random.randint(20, 50, size=(random.randint(3, 5), random.randint(3, 5)))
            array2 = np.random.randint(3, 10, size=array1.shape)
            question = f"Given: array1 = \n{array1}, array2 = \n{array2}\nWrite the code to compute element-wise modulo"
            answer = "np.mod(array1, array2)"
        hint = "NumPy arithmetic functions work element-wise on multi-dimensional arrays"
    
    return {"type": "arithmetic", "question": question, "answer": answer, "hint": hint}


def generate_rounding_challenge(difficulty="easy"):
    """Generate challenge for rounding operations"""
    question_type = random.choice(["round", "floor", "ceil", "trunc"])
    
    if difficulty == "easy":
        if question_type == "round":
            value = round(random.uniform(1.0, 10.0), 2)
            decimals = random.randint(0, 2)
            question = f"Write the code to round {value} to {decimals} decimal places using NumPy"
            answer = f"np.round({value}, {decimals})"
        elif question_type == "floor":
            value = round(random.uniform(1.0, 10.0), 2)
            question = f"Write the code to round {value} down to the nearest integer using NumPy"
            answer = f"np.floor({value})"
        elif question_type == "ceil":
            value = round(random.uniform(1.0, 10.0), 2)
            question = f"Write the code to round {value} up to the nearest integer using NumPy"
            answer = f"np.ceil({value})"
        else:  # trunc
            value = round(random.uniform(1.0, 10.0), 2)
            question = f"Write the code to truncate {value} (remove decimal part) using NumPy"
            answer = f"np.trunc({value})"
        hint = "NumPy has functions to round numbers: round, floor, ceil, trunc"
    elif difficulty == "medium":
        if question_type == "round":
            array = np.random.uniform(1.0, 20.0, size=random.randint(5, 8))
            decimals = random.randint(0, 2)
            question = f"Given: array = {array}\nWrite the code to round each element to {decimals} decimal places"
            answer = f"np.round(array, {decimals})"
        elif question_type == "floor":
            array = np.random.uniform(1.0, 20.0, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to round each element down to the nearest integer"
            answer = "np.floor(array)"
        elif question_type == "ceil":
            array = np.random.uniform(1.0, 20.0, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to round each element up to the nearest integer"
            answer = "np.ceil(array)"
        else:  # trunc
            array = np.random.uniform(1.0, 20.0, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to truncate each element (remove decimal part)"
            answer = "np.trunc(array)"
        hint = "Rounding functions work element-wise on arrays"
    else:  # hard
        if question_type == "round":
            array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
            decimals = random.randint(0, 3)
            question = f"Given: array = \n{array}\nWrite the code to round each element to {decimals} decimal places"
            answer = f"np.round(array, {decimals})"
        elif question_type == "floor":
            array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to round each element down to the nearest integer"
            answer = "np.floor(array)"
        elif question_type == "ceil":
            array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to round each element up to the nearest integer"
            answer = "np.ceil(array)"
        else:  # trunc
            array = np.random.uniform(1.0, 50.0, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to truncate each element (remove decimal part)"
            answer = "np.trunc(array)"
        hint = "Rounding functions work element-wise on multi-dimensional arrays"
    
    return {"type": "rounding", "question": question, "answer": answer, "hint": hint}


def generate_logarithm_challenge(difficulty="easy"):
    """Generate challenge for logarithm operations"""
    question_type = random.choice(["log", "log10", "log2", "exp"])
    
    if difficulty == "easy":
        if question_type == "log":
            value = random.randint(2, 10)
            question = f"Write the code to compute the natural logarithm (base e) of {value} using NumPy"
            answer = f"np.log({value})"
        elif question_type == "log10":
            value = random.choice([10, 100, 1000])
            question = f"Write the code to compute the base-10 logarithm of {value} using NumPy"
            answer = f"np.log10({value})"
        elif question_type == "log2":
            value = random.choice([2, 4, 8, 16, 32])
            question = f"Write the code to compute the base-2 logarithm of {value} using NumPy"
            answer = f"np.log2({value})"
        else:  # exp
            value = random.randint(1, 5)
            question = f"Write the code to compute e raised to the power of {value} using NumPy"
            answer = f"np.exp({value})"
        hint = "NumPy has log, log10, log2 for logarithms and exp for exponential"
    elif difficulty == "medium":
        if question_type == "log":
            array = np.random.randint(1, 20, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the natural logarithm of each element"
            answer = "np.log(array)"
        elif question_type == "log10":
            array = np.random.randint(1, 100, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the base-10 logarithm of each element"
            answer = "np.log10(array)"
        elif question_type == "log2":
            array = np.random.randint(1, 32, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the base-2 logarithm of each element"
            answer = "np.log2(array)"
        else:  # exp
            array = np.random.uniform(0.1, 3.0, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute e raised to the power of each element"
            answer = "np.exp(array)"
        hint = "Logarithm functions work element-wise on arrays"
    else:  # hard
        if question_type == "log":
            array = np.random.randint(1, 50, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to compute the natural logarithm of each element"
            answer = "np.log(array)"
        elif question_type == "log10":
            array = np.random.randint(1, 1000, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to compute the base-10 logarithm of each element"
            answer = "np.log10(array)"
        elif question_type == "log2":
            array = np.random.randint(1, 64, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to compute the base-2 logarithm of each element"
            answer = "np.log2(array)"
        else:  # exp
            array = np.random.uniform(0.1, 4.0, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to compute e raised to the power of each element"
            answer = "np.exp(array)"
        hint = "Logarithm functions work element-wise on multi-dimensional arrays"
    
    return {"type": "logarithm", "question": question, "answer": answer, "hint": hint}


def generate_summation_challenge(difficulty="easy"):
    """Generate challenge for summation"""
    question_type = random.choice(["sum", "cumsum", "axis"])
    
    if difficulty == "easy":
        if question_type == "sum":
            array = np.random.randint(1, 10, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the sum of all elements"
            answer = "np.sum(array)"
        elif question_type == "cumsum":
            array = np.random.randint(1, 10, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the cumulative sum"
            answer = "np.cumsum(array)"
        else:  # axis
            array = np.random.randint(1, 10, size=(random.randint(3, 4), random.randint(3, 4)))
            axis = random.choice([0, 1])
            question = f"Given: array = \n{array}\nWrite the code to sum along axis {axis}"
            answer = f"np.sum(array, axis={axis})"
        hint = "np.sum() computes the sum of array elements"
    elif difficulty == "medium":
        if question_type == "sum":
            array = np.random.randint(1, 20, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to compute the sum of all elements"
            answer = "np.sum(array)"
        elif question_type == "cumsum":
            array = np.random.randint(1, 20, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to compute the cumulative sum"
            answer = "np.cumsum(array)"
        else:  # axis
            array = np.random.randint(1, 20, size=(random.randint(4, 6), random.randint(4, 6)))
            axis = random.choice([0, 1])
            question = f"Given: array = \n{array}\nWrite the code to sum along axis {axis}"
            answer = f"np.sum(array, axis={axis})"
        hint = "You can specify axis parameter to sum along specific dimensions"
    else:  # hard
        if question_type == "sum":
            array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
            question = f"Given: array = \n{array}\nWrite the code to compute the sum of all elements"
            answer = "np.sum(array)"
        elif question_type == "cumsum":
            array = np.random.randint(1, 50, size=random.randint(10, 15))
            question = f"Given: array = {array}\nWrite the code to compute the cumulative sum"
            answer = "np.cumsum(array)"
        else:  # axis
            array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
            axis = random.choice([0, 1])
            question = f"Given: array = \n{array}\nWrite the code to sum along axis {axis}"
            answer = f"np.sum(array, axis={axis})"
        hint = "Axis 0 sums along rows, axis 1 sums along columns"
    
    return {"type": "summation", "question": question, "answer": answer, "hint": hint}


def generate_product_challenge(difficulty="easy"):
    """Generate challenge for product"""
    question_type = random.choice(["prod", "cumprod", "axis"])
    
    if difficulty == "easy":
        if question_type == "prod":
            array = np.random.randint(1, 5, size=random.randint(4, 6))
            question = f"Given: array = {array}\nWrite the code to compute the product of all elements"
            answer = "np.prod(array)"
        elif question_type == "cumprod":
            array = np.random.randint(1, 5, size=random.randint(4, 6))
            question = f"Given: array = {array}\nWrite the code to compute the cumulative product"
            answer = "np.cumprod(array)"
        else:  # axis
            array = np.random.randint(1, 5, size=(random.randint(3, 4), random.randint(3, 4)))
            axis = random.choice([0, 1])
            question = f"Given: array = \n{array}\nWrite the code to compute product along axis {axis}"
            answer = f"np.prod(array, axis={axis})"
        hint = "np.prod() computes the product of array elements"
    elif difficulty == "medium":
        if question_type == "prod":
            array = np.random.randint(1, 10, size=random.randint(6, 10))
            question = f"Given: array = {array}\nWrite the code to compute the product of all elements"
            answer = "np.prod(array)"
        elif question_type == "cumprod":
            array = np.random.randint(1, 10, size=random.randint(6, 10))
            question = f"Given: array = {array}\nWrite the code to compute the cumulative product"
            answer = "np.cumprod(array)"
        else:  # axis
            array = np.random.randint(1, 10, size=(random.randint(4, 5), random.randint(4, 5)))
            axis = random.choice([0, 1])
            question = f"Given: array = \n{array}\nWrite the code to compute product along axis {axis}"
            answer = f"np.prod(array, axis={axis})"
        hint = "You can specify axis parameter to compute product along specific dimensions"
    else:  # hard
        if question_type == "prod":
            array = np.random.randint(1, 20, size=(random.randint(4, 5), random.randint(4, 5)))
            question = f"Given: array = \n{array}\nWrite the code to compute the product of all elements"
            answer = "np.prod(array)"
        elif question_type == "cumprod":
            array = np.random.randint(1, 20, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to compute the cumulative product"
            answer = "np.cumprod(array)"
        else:  # axis
            array = np.random.randint(1, 20, size=(random.randint(4, 6), random.randint(4, 6)))
            axis = random.choice([0, 1])
            question = f"Given: array = \n{array}\nWrite the code to compute product along axis {axis}"
            answer = f"np.prod(array, axis={axis})"
        hint = "Axis 0 computes product along rows, axis 1 along columns"
    
    return {"type": "product", "question": question, "answer": answer, "hint": hint}


def generate_difference_challenge(difficulty="easy"):
    """Generate challenge for differences"""
    question_type = random.choice(["diff", "gradient", "ediff1d"])
    
    if difficulty == "easy":
        if question_type == "diff":
            array = np.random.randint(1, 20, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the differences between consecutive elements"
            answer = "np.diff(array)"
        elif question_type == "gradient":
            array = np.random.randint(1, 20, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the gradient (differences)"
            answer = "np.gradient(array)"
        else:  # ediff1d
            array = np.random.randint(1, 20, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to compute the differences (ediff1d)"
            answer = "np.ediff1d(array)"
        hint = "np.diff() computes differences between consecutive elements"
    elif difficulty == "medium":
        if question_type == "diff":
            array = np.random.randint(1, 30, size=random.randint(8, 12))
            n = random.randint(1, 2)
            question = f"Given: array = {array}\nWrite the code to compute the {n}-th order differences"
            answer = f"np.diff(array, n={n})"
        elif question_type == "gradient":
            array = np.random.randint(1, 30, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to compute the gradient"
            answer = "np.gradient(array)"
        else:  # ediff1d
            array = np.random.randint(1, 30, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to compute element-wise differences"
            answer = "np.ediff1d(array)"
        hint = "You can specify the order of differences with the n parameter"
    else:  # hard
        if question_type == "diff":
            array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
            axis = random.choice([0, 1])
            question = f"Given: array = \n{array}\nWrite the code to compute differences along axis {axis}"
            answer = f"np.diff(array, axis={axis})"
        elif question_type == "gradient":
            array = np.random.randint(1, 50, size=(random.randint(4, 6), random.randint(4, 6)))
            question = f"Given: array = \n{array}\nWrite the code to compute the gradient"
            answer = "np.gradient(array)"
        else:  # ediff1d
            array = np.random.randint(1, 50, size=random.randint(10, 15))
            question = f"Given: array = {array}\nWrite the code to compute element-wise differences"
            answer = "np.ediff1d(array)"
        hint = "You can compute differences along specific axes for 2D arrays"
    
    return {"type": "difference", "question": question, "answer": answer, "hint": hint}


def generate_lcm_gcd_challenge(difficulty="easy"):
    """Generate challenge for LCM and GCD"""
    question_type = random.choice(["gcd", "lcm", "array_gcd", "array_lcm"])
    
    if difficulty == "easy":
        if question_type == "gcd":
            a = random.randint(10, 30)
            b = random.randint(10, 30)
            question = f"Write the code to find the GCD (greatest common divisor) of {a} and {b} using NumPy"
            answer = f"np.gcd({a}, {b})"
        elif question_type == "lcm":
            a = random.randint(5, 20)
            b = random.randint(5, 20)
            question = f"Write the code to find the LCM (least common multiple) of {a} and {b} using NumPy"
            answer = f"np.lcm({a}, {b})"
        elif question_type == "array_gcd":
            array = np.random.randint(10, 30, size=random.randint(4, 6))
            question = f"Given: array = {array}\nWrite the code to find GCD of all elements (reduce)"
            answer = "np.gcd.reduce(array)"
        else:  # array_lcm
            array = np.random.randint(5, 20, size=random.randint(4, 6))
            question = f"Given: array = {array}\nWrite the code to find LCM of all elements (reduce)"
            answer = "np.lcm.reduce(array)"
        hint = "NumPy has gcd() and lcm() functions for finding common divisors and multiples"
    elif difficulty == "medium":
        if question_type == "gcd":
            a = random.randint(20, 50)
            b = random.randint(20, 50)
            question = f"Write the code to find the GCD of {a} and {b} using NumPy"
            answer = f"np.gcd({a}, {b})"
        elif question_type == "lcm":
            a = random.randint(10, 40)
            b = random.randint(10, 40)
            question = f"Write the code to find the LCM of {a} and {b} using NumPy"
            answer = f"np.lcm({a}, {b})"
        elif question_type == "array_gcd":
            array = np.random.randint(20, 50, size=random.randint(6, 10))
            question = f"Given: array = {array}\nWrite the code to find GCD of all elements"
            answer = "np.gcd.reduce(array)"
        else:  # array_lcm
            array = np.random.randint(10, 40, size=random.randint(6, 10))
            question = f"Given: array = {array}\nWrite the code to find LCM of all elements"
            answer = "np.lcm.reduce(array)"
        hint = "Use .reduce() to apply gcd/lcm across all elements of an array"
    else:  # hard
        if question_type == "gcd":
            a = random.randint(50, 100)
            b = random.randint(50, 100)
            c = random.randint(50, 100)
            question = f"Write the code to find the GCD of {a}, {b}, and {c} using NumPy"
            answer = f"np.gcd.reduce([{a}, {b}, {c}])"
        elif question_type == "lcm":
            a = random.randint(20, 60)
            b = random.randint(20, 60)
            c = random.randint(20, 60)
            question = f"Write the code to find the LCM of {a}, {b}, and {c} using NumPy"
            answer = f"np.lcm.reduce([{a}, {b}, {c}])"
        elif question_type == "array_gcd":
            array = np.random.randint(50, 100, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to find GCD of all elements"
            answer = "np.gcd.reduce(array)"
        else:  # array_lcm
            array = np.random.randint(20, 60, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to find LCM of all elements"
            answer = "np.lcm.reduce(array)"
        hint = "Use .reduce() to apply gcd/lcm across multiple values or array elements"
    
    return {"type": "lcm_gcd", "question": question, "answer": answer, "hint": hint}


def generate_set_operations_challenge(difficulty="easy"):
    """Generate challenge for set operations"""
    question_type = random.choice(["unique", "intersect", "union", "setdiff", "setxor"])
    
    if difficulty == "easy":
        if question_type == "unique":
            array = np.random.randint(1, 10, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to get unique values"
            answer = "np.unique(array)"
        elif question_type == "intersect":
            array1 = np.random.randint(1, 10, size=random.randint(5, 8))
            array2 = np.random.randint(1, 10, size=random.randint(5, 8))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find common elements"
            answer = "np.intersect1d(array1, array2)"
        elif question_type == "union":
            array1 = np.random.randint(1, 10, size=random.randint(5, 8))
            array2 = np.random.randint(1, 10, size=random.randint(5, 8))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find all unique elements from both arrays"
            answer = "np.union1d(array1, array2)"
        elif question_type == "setdiff":
            array1 = np.random.randint(1, 10, size=random.randint(5, 8))
            array2 = np.random.randint(1, 10, size=random.randint(5, 8))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find elements in array1 but not in array2"
            answer = "np.setdiff1d(array1, array2)"
        else:  # setxor
            array1 = np.random.randint(1, 10, size=random.randint(5, 8))
            array2 = np.random.randint(1, 10, size=random.randint(5, 8))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find elements in either array but not both"
            answer = "np.setxor1d(array1, array2)"
        hint = "NumPy has functions for set operations: unique, intersect1d, union1d, setdiff1d"
    elif difficulty == "medium":
        if question_type == "unique":
            array = np.random.randint(1, 20, size=random.randint(10, 15))
            question = f"Given: array = {array}\nWrite the code to get unique values"
            answer = "np.unique(array)"
        elif question_type == "intersect":
            array1 = np.random.randint(1, 20, size=random.randint(8, 12))
            array2 = np.random.randint(1, 20, size=random.randint(8, 12))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find common elements"
            answer = "np.intersect1d(array1, array2)"
        elif question_type == "union":
            array1 = np.random.randint(1, 20, size=random.randint(8, 12))
            array2 = np.random.randint(1, 20, size=random.randint(8, 12))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find all unique elements from both arrays"
            answer = "np.union1d(array1, array2)"
        elif question_type == "setdiff":
            array1 = np.random.randint(1, 20, size=random.randint(8, 12))
            array2 = np.random.randint(1, 20, size=random.randint(8, 12))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find elements in array1 but not in array2"
            answer = "np.setdiff1d(array1, array2)"
        else:  # setxor
            array1 = np.random.randint(1, 20, size=random.randint(8, 12))
            array2 = np.random.randint(1, 20, size=random.randint(8, 12))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find elements in either array but not both"
            answer = "np.setxor1d(array1, array2)"
        hint = "Set operations work on 1D arrays and return sorted unique results"
    else:  # hard
        if question_type == "unique":
            array = np.random.randint(1, 50, size=random.randint(15, 25))
            question = f"Given: array = {array}\nWrite the code to get unique values"
            answer = "np.unique(array)"
        elif question_type == "intersect":
            array1 = np.random.randint(1, 50, size=random.randint(12, 18))
            array2 = np.random.randint(1, 50, size=random.randint(12, 18))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find common elements"
            answer = "np.intersect1d(array1, array2)"
        elif question_type == "union":
            array1 = np.random.randint(1, 50, size=random.randint(12, 18))
            array2 = np.random.randint(1, 50, size=random.randint(12, 18))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find all unique elements from both arrays"
            answer = "np.union1d(array1, array2)"
        elif question_type == "setdiff":
            array1 = np.random.randint(1, 50, size=random.randint(12, 18))
            array2 = np.random.randint(1, 50, size=random.randint(12, 18))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find elements in array1 but not in array2"
            answer = "np.setdiff1d(array1, array2)"
        else:  # setxor
            array1 = np.random.randint(1, 50, size=random.randint(12, 18))
            array2 = np.random.randint(1, 50, size=random.randint(12, 18))
            question = f"Given: array1 = {array1}, array2 = {array2}\nWrite the code to find elements in either array but not both"
            answer = "np.setxor1d(array1, array2)"
        hint = "Set operations return sorted unique arrays"
    
    return {"type": "set_operations", "question": question, "answer": answer, "hint": hint}


def generate_true_false_challenge(difficulty="easy", *, used_questions=None):
    """Generate true/false questions about ufunc operations."""
    statements_by_difficulty = {
        "easy": [
            ("True or False: np.add(a, b) performs element-wise addition when a and b are arrays.", "true"),
            ("True or False: np.round(3.7) returns 4.", "true"),
            ("True or False: np.log10(100) returns 2.", "true"),
            ("True or False: np.sum(array) adds all elements in the array.", "true"),
            ("True or False: np.prod(array) multiplies all elements in the array.", "true"),
            ("True or False: np.log10(10) returns 10.", "false"),
            ("True or False: np.ceil(2.1) returns 2.", "false"),
        ],
        "medium": [
            ("True or False: np.multiply() and * operator perform the same element-wise multiplication.", "true"),
            ("True or False: np.floor(3.7) returns 3.0.", "true"),
            ("True or False: np.log(1) returns 0.", "true"),
            ("True or False: np.sum(array, axis=0) sums along the first axis (rows).", "true"),
            ("True or False: np.prod(array) returns 0 if any element is 0.", "true"),
            ("True or False: np.diff(array) returns an array with one fewer element than the original.", "true"),
            ("True or False: np.gcd(12, 18) returns 6.", "true"),
            ("True or False: np.unique(array) returns sorted unique values.", "true"),
            ("True or False: All NumPy arithmetic ufuncs work element-wise on arrays.", "true"),
            ("True or False: np.log(10) returns 1.", "false"),
            ("True or False: np.gcd(4, 6, 8) accepts three integers in one call and returns their overall GCD.", "false"),
        ],
        "hard": [
            ("True or False: np.divide() can handle broadcasting when array shapes are compatible.", "true"),
            ("True or False: np.trunc() and np.floor() always return the same result for positive numbers.", "true"),
            ("True or False: np.exp(np.log(x)) returns x for positive x.", "true"),
            ("True or False: np.cumsum(array) returns the cumulative sum as a new array.", "true"),
            ("True or False: np.cumprod(array) computes the cumulative product.", "true"),
            ("True or False: np.diff(array, n=2) computes second-order differences.", "true"),
            ("True or False: np.lcm.reduce([4, 6, 8]) finds the LCM of all three numbers.", "true"),
            ("True or False: np.setdiff1d(a, b) returns elements in a but not in b.", "true"),
            ("True or False: Ufuncs automatically broadcast arrays with compatible shapes.", "true"),
            ("True or False: Aggregation functions like sum() and prod() can operate along specific axes.", "true"),
            ("True or False: np.prod on an empty array returns 0.", "false"),
            ("True or False: np.trunc(x) and np.floor(x) always return the same value for every x.", "false"),
        ],
    }
    hints_by_difficulty = {
        "easy": "Think about how NumPy ufuncs work",
        "medium": "Consider how ufuncs operate on arrays",
        "hard": "Advanced ufunc operations involve broadcasting and axis handling",
    }
    question, answer, hint = pick_true_false_statement(
        difficulty, statements_by_difficulty, hints_by_difficulty, used_questions=used_questions
    )
    return {"type": "true_false", "question": question, "answer": answer, "hint": hint}


def validate_code_answer(user_input, correct_answer):
    """Validate user's code answer using shared default profile."""
    return shared_validate_code_answer(user_input, correct_answer, profile="default")


def show_hint(challenge):
    """Display a hint for the current challenge."""
    print(f"Hint: {challenge['hint']}")


def play_game():
    """Run a single game session."""

    challenge_functions = [
        generate_arithmetic_challenge,
        generate_rounding_challenge,
        generate_logarithm_challenge,
        generate_summation_challenge,
        generate_product_challenge,
        generate_difference_challenge,
        generate_lcm_gcd_challenge,
        generate_set_operations_challenge,
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
        game_name="Ufunc Arena",
        subtitle="Master NumPy Universal Functions!",
        perfect_message="Perfect score! You're a ufunc master! 🎉",
        thank_you_message="Thank you for playing Ufunc Arena!",
        code_validator=validate_code_answer,
        sequence_builder=build_sequence,
        show_hint=show_hint,
    )


def main():
    """Main game loop with play-again prompt."""
    run_with_replay(play_game)


if __name__ == "__main__":
    main()