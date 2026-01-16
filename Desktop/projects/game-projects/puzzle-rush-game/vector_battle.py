import numpy as np
import random

"""
Vector Battle - Master NumPy random operations and permutations

This game challenges you to:
- Understand np.random.permutation() vs np.random.shuffle()
- Work with random number generation
- Understand data distributions
- Use np.random.choice() and np.random.randint()
"""


def generate_permutation_challenge(difficulty="easy"):
    """Generate challenge for np.random.permutation()"""
    question_type = random.choice(["create", "range", "property"])
    
    if difficulty == "easy":
        if question_type == "create":
            array = np.array([1, 2, 3, 4, 5])
            question = f"Given: array = {array}\nWrite the code to randomly rearrange this array (returns new array)"
            answer = "np.random.permutation(array)"
        elif question_type == "range":
            size = random.randint(5, 10)
            question = f"Write the code to randomly permute integers from 0 to {size-1}"
            answer = f"np.random.permutation({size})"
        else:  # property
            question = "What function randomly rearranges an array and returns a new array (doesn't modify original)?\nWrite the function name"
            answer = "np.random.permutation"
        hint = "What function randomly rearranges elements and returns a new array?"
    elif difficulty == "medium":
        if question_type == "create":
            array = np.random.randint(0, 15, size=random.randint(6, 10))
            question = f"Given: array = {array}\nWrite the code to get a shuffled version without changing the original"
            answer = "np.random.permutation(array)"
        elif question_type == "range":
            size = random.randint(8, 15)
            question = f"Write the code to create a random arrangement of numbers 0 through {size-1}"
            answer = f"np.random.permutation({size})"
        else:  # property
            question = "Which NumPy function creates a new randomly ordered array from an existing one?\nWrite the function name"
            answer = "np.random.permutation"
        hint = "permutation can take an integer to permute a range"
    else:  # hard
        question_type = random.choice(["create", "range", "property", "2d", "copy", "scenario"])
        if question_type == "create":
            array = np.random.randint(0, 20, size=random.randint(8, 15))
            question = f"Given: array = {array}\nWrite the code to generate a permuted copy (original stays unchanged)"
            answer = "np.random.permutation(array)"
        elif question_type == "range":
            size = random.randint(10, 20)
            question = f"Write the code to randomly order the sequence [0, 1, 2, ..., {size-1}]"
            answer = f"np.random.permutation({size})"
        elif question_type == "property":
            question = "What is the return value type of np.random.permutation(array)?\nWrite 'array' or 'none'"
            answer = "array"
        elif question_type == "2d":
            array = np.random.randint(0, 30, size=(random.randint(3, 5), random.randint(3, 5)))
            question = f"Given: array = \n{array}\nWrite the code to permute the rows (returns new array)"
            answer = "np.random.permutation(array)"
        elif question_type == "copy":
            array = np.random.randint(0, 25, size=random.randint(10, 15))
            question = f"Given: array = {array}\nYou need a shuffled version but must preserve the original. Write the code"
            answer = "np.random.permutation(array)"
        else:  # scenario
            question = "You have an array and need to create multiple independent shuffled versions. Which function should you use?\nWrite the function name (permutation or shuffle)"
            answer = "permutation"
        hint = "permutation returns a new array, it doesn't modify the original"
    
    return {"type": "permutation", "question": question, "answer": answer, "hint": hint}


def generate_shuffle_challenge(difficulty="easy"):
    """Generate challenge for np.random.shuffle()"""
    question_type = random.choice(["inplace", "property", "modify"])
    
    if difficulty == "easy":
        if question_type == "inplace":
            array = np.array([1, 2, 3, 4, 5])
            question = f"Given: array = {array}\nWrite the code to randomly reorder this array (modifies it directly)"
            answer = "np.random.shuffle(array)"
        elif question_type == "property":
            question = "What function randomly rearranges an array and modifies the original?\nWrite the function name"
            answer = "np.random.shuffle"
        else:  # modify
            array = np.random.randint(0, 10, size=random.randint(5, 8))
            question = f"Given: array = {array}\nWrite the code to change the order of elements in-place"
            answer = "np.random.shuffle(array)"
        hint = "What function randomly rearranges elements and modifies the array directly?"
    elif difficulty == "medium":
        if question_type == "inplace":
            array = np.random.randint(0, 20, size=random.randint(6, 12))
            question = f"Given: array = {array}\nWrite the code to randomly rearrange it (changes original array)"
            answer = "np.random.shuffle(array)"
        elif question_type == "property":
            question = "What does np.random.shuffle() return?\nWrite 'none' or 'array'"
            answer = "none"
        else:  # modify
            array = np.random.randint(0, 15, size=random.randint(8, 12))
            question = f"Given: array = {array}\nWrite the code to mix up the elements (alters the original)"
            answer = "np.random.shuffle(array)"
        hint = "shuffle modifies the array in-place, unlike permutation"
    else:  # hard
        question_type = random.choice(["inplace", "property", "modify", "2d", "memory", "scenario"])
        if question_type == "inplace":
            array = np.random.randint(0, 50, size=(random.randint(3, 6), random.randint(3, 6)))
            question = f"Given: array = \n{array}\nWrite the code to shuffle rows (modifies original)"
            answer = "np.random.shuffle(array)"
        elif question_type == "property":
            question = "Which function modifies arrays in-place and returns None?\nWrite the function name"
            answer = "np.random.shuffle"
        elif question_type == "modify":
            array = np.random.randint(0, 30, size=random.randint(10, 15))
            question = f"Given: array = {array}\nWrite the code to randomly reorder elements (destructive operation)"
            answer = "np.random.shuffle(array)"
        elif question_type == "2d":
            array = np.random.randint(0, 40, size=(random.randint(4, 6), random.randint(4, 6)))
            question = f"Given: array = \n{array}\nWrite the code to randomly rearrange rows in-place (no copy created)"
            answer = "np.random.shuffle(array)"
        elif question_type == "memory":
            question = "You want to shuffle a large array without creating a copy to save memory. Write the code"
            answer = "np.random.shuffle(array)"
        else:  # scenario
            question = "You need to shuffle an array and don't need the original order. Which function is more memory-efficient?\nWrite the function name (permutation or shuffle)"
            answer = "shuffle"
        hint = "shuffle works along the first axis by default for 2D arrays"
    
    return {"type": "shuffle", "question": question, "answer": answer, "hint": hint}


def generate_distribution_challenge(difficulty="easy"):
    """Generate challenge for random number generation"""
    question_type = random.choice(["single", "multiple", "range", "negative"])
    
    if difficulty == "easy":
        if question_type == "single":
            low = random.randint(1, 5)
            high = random.randint(6, 15)
            question = f"Write the code to generate a random integer between {low} and {high-1} (inclusive)"
            answer = f"np.random.randint({low}, {high})"
        elif question_type == "multiple":
            low = random.randint(0, 5)
            high = random.randint(6, 12)
            size = random.randint(3, 6)
            question = f"Write the code to generate {size} random integers from {low} to {high-1}"
            answer = f"np.random.randint({low}, {high}, size={size})"
        elif question_type == "range":
            high = random.randint(5, 10)
            question = f"Write the code to generate a random integer from 0 to {high-1}"
            answer = f"np.random.randint({high})"
        else:  # negative
            low = random.randint(-5, -1)
            high = random.randint(1, 5)
            question = f"Write the code to generate a random integer between {low} and {high-1}"
            answer = f"np.random.randint({low}, {high})"
        hint = "What function generates random integers in a range?"
    elif difficulty == "medium":
        if question_type == "single":
            low = random.randint(-10, 0)
            high = random.randint(1, 20)
            question = f"Write the code to generate a random integer between {low} and {high-1}"
            answer = f"np.random.randint({low}, {high})"
        elif question_type == "multiple":
            low = random.randint(-10, 0)
            high = random.randint(1, 20)
            size = random.randint(5, 10)
            question = f"Write the code to create an array of {size} random integers from {low} to {high-1}"
            answer = f"np.random.randint({low}, {high}, size={size})"
        elif question_type == "range":
            high = random.randint(10, 20)
            size = random.randint(5, 8)
            question = f"Write the code to generate {size} random integers from 0 to {high-1}"
            answer = f"np.random.randint({high}, size={size})"
        else:  # negative
            low = random.randint(-15, -5)
            high = random.randint(5, 15)
            size = random.randint(6, 10)
            question = f"Write the code to generate {size} random integers between {low} and {high-1}"
            answer = f"np.random.randint({low}, {high}, size={size})"
        hint = "You can specify the size parameter to generate multiple values"
    else:  # hard
        question_type = random.choice(["single", "multiple", "range", "negative", "3d", "large", "edge"])
        if question_type == "single":
            low = random.randint(-20, 0)
            high = random.randint(1, 50)
            question = f"Write the code to generate a random integer between {low} and {high-1}"
            answer = f"np.random.randint({low}, {high})"
        elif question_type == "multiple":
            low = random.randint(-20, 0)
            high = random.randint(1, 50)
            shape = (random.randint(3, 5), random.randint(3, 5))
            question = f"Write the code to generate a 2D array with shape {shape} of random integers from {low} to {high-1}"
            answer = f"np.random.randint({low}, {high}, size={shape})"
        elif question_type == "range":
            high = random.randint(20, 40)
            shape = (random.randint(3, 5), random.randint(3, 5))
            question = f"Write the code to generate a 2D array with shape {shape} of random integers from 0 to {high-1}"
            answer = f"np.random.randint({high}, size={shape})"
        elif question_type == "negative":
            low = random.randint(-30, -10)
            high = random.randint(10, 40)
            shape = (random.randint(4, 6), random.randint(4, 6))
            question = f"Write the code to generate a 2D array with shape {shape} of random integers between {low} and {high-1}"
            answer = f"np.random.randint({low}, {high}, size={shape})"
        elif question_type == "3d":
            low = random.randint(-10, 0)
            high = random.randint(1, 30)
            shape = (random.randint(2, 3), random.randint(2, 3), random.randint(2, 3))
            question = f"Write the code to generate a 3D array with shape {shape} of random integers from {low} to {high-1}"
            answer = f"np.random.randint({low}, {high}, size={shape})"
        elif question_type == "large":
            low = random.randint(-50, -20)
            high = random.randint(20, 100)
            size = random.randint(15, 25)
            question = f"Write the code to generate {size} random integers between {low} and {high-1}"
            answer = f"np.random.randint({low}, {high}, size={size})"
        else:  # edge
            question = "Write the code to generate a random integer from 0 to 99 (inclusive)"
            answer = "np.random.randint(100)"
            hint = "When only one argument is given, it generates from 0 to that value (exclusive)"
        if question_type != "edge":
            hint = "The size parameter can be a tuple for multi-dimensional arrays"
    
    return {"type": "distribution", "question": question, "answer": answer, "hint": hint}


def generate_choice_challenge(difficulty="easy"):
    """Generate challenge for np.random.choice()"""
    question_type = random.choice(["single", "multiple", "replace", "weights"])
    
    if difficulty == "easy":
        if question_type == "single":
            array = np.array([1, 2, 3, 4, 5])
            question = f"Given: array = {array}\nWrite the code to randomly pick one element from this array"
            answer = "np.random.choice(array)"
        elif question_type == "multiple":
            array = np.random.randint(0, 10, size=random.randint(5, 8))
            size = random.randint(2, 3)
            question = f"Given: array = {array}\nWrite the code to randomly select {size} elements"
            answer = f"np.random.choice(array, size={size})"
        elif question_type == "replace":
            array = np.array([1, 2, 3, 4, 5])
            question = f"Given: array = {array}\nWrite the code to randomly pick one element (can repeat)"
            answer = "np.random.choice(array)"
        else:  # weights
            array = np.array([1, 2, 3, 4, 5])
            question = f"Given: array = {array}\nWrite the code to randomly choose one element"
            answer = "np.random.choice(array)"
        hint = "What function randomly picks from an array?"
    elif difficulty == "medium":
        if question_type == "single":
            array = np.random.randint(0, 20, size=random.randint(5, 10))
            question = f"Given: array = {array}\nWrite the code to randomly pick one value"
            answer = "np.random.choice(array)"
        elif question_type == "multiple":
            array = np.random.randint(0, 20, size=random.randint(5, 10))
            size = random.randint(2, 4)
            question = f"Given: array = {array}\nWrite the code to randomly select {size} elements (with replacement)"
            answer = f"np.random.choice(array, size={size})"
        elif question_type == "replace":
            array = np.random.randint(0, 15, size=random.randint(6, 10))
            size = random.randint(3, 5)
            question = f"Given: array = {array}\nWrite the code to randomly pick {size} elements (allow duplicates)"
            answer = f"np.random.choice(array, size={size}, replace=True)"
        else:  # weights
            array = np.random.randint(0, 20, size=random.randint(5, 8))
            size = random.randint(2, 3)
            question = f"Given: array = {array}\nWrite the code to randomly select {size} elements"
            answer = f"np.random.choice(array, size={size})"
        hint = "You can select multiple elements by specifying size"
    else:  # hard
        question_type = random.choice(["single", "multiple", "replace", "weights", "large", "unique", "scenario"])
        if question_type == "single":
            array = np.random.randint(0, 50, size=random.randint(8, 15))
            question = f"Given: array = {array}\nWrite the code to randomly choose one element"
            answer = "np.random.choice(array)"
        elif question_type == "multiple":
            array = np.random.randint(0, 50, size=random.randint(8, 15))
            size = random.randint(3, 6)
            question = f"Given: array = {array}\nWrite the code to randomly select {size} elements"
            answer = f"np.random.choice(array, size={size})"
        elif question_type == "replace":
            array = np.random.randint(0, 50, size=random.randint(8, 15))
            size = random.randint(3, 6)
            replace = random.choice([True, False])
            question = f"Given: array = {array}\nWrite the code to randomly select {size} elements (replace={replace})"
            answer = f"np.random.choice(array, size={size}, replace={replace})"
        elif question_type == "weights":
            array = np.random.randint(0, 50, size=random.randint(8, 12))
            size = random.randint(3, 5)
            question = f"Given: array = {array}\nWrite the code to randomly pick {size} elements without replacement"
            answer = f"np.random.choice(array, size={size}, replace=False)"
        elif question_type == "large":
            array = np.random.randint(0, 100, size=random.randint(15, 25))
            size = random.randint(5, 10)
            question = f"Given: array = {array}\nWrite the code to randomly select {size} elements (with replacement)"
            answer = f"np.random.choice(array, size={size})"
        elif question_type == "unique":
            array = np.random.randint(0, 50, size=random.randint(10, 15))
            size = random.randint(4, 7)
            question = f"Given: array = {array}\nWrite the code to randomly pick {size} unique elements (no duplicates)"
            answer = f"np.random.choice(array, size={size}, replace=False)"
        else:  # scenario
            array_size = random.randint(8, 12)
            array = np.random.randint(0, 30, size=array_size)
            sample_size = array_size + 3
            question = f"Given: array = {array}\nYou need to sample more elements than the array size. Write the code to select {sample_size} elements"
            answer = f"np.random.choice(array, size={sample_size}, replace=True)"
        hint = "The replace parameter controls whether elements can be selected multiple times"
    
    return {"type": "choice", "question": question, "answer": answer, "hint": hint}


def generate_comparison_challenge(difficulty="easy"):
    """Generate challenge comparing shuffle vs permutation"""
    question_type = random.choice(["difference", "use_case", "return", "property"])
    
    if difficulty == "easy":
        if question_type == "difference":
            if random.choice([True, False]):
                question = "Which function returns a new array instead of modifying the original?\nWrite the function name (permutation or shuffle)"
                answer = "permutation"
            else:
                question = "Which function modifies the array in-place (changes the original)?\nWrite the function name (permutation or shuffle)"
                answer = "shuffle"
            hint = "One returns a new array, the other modifies the original"
        elif question_type == "use_case":
            array = np.array([1, 2, 3, 4, 5])
            question = f"Given: array = {array}\nWrite the code to get a shuffled version without changing the original"
            answer = "np.random.permutation(array)"
            hint = "If you want to keep the original unchanged, use the one that returns a new array"
        elif question_type == "return":
            question = "What does np.random.shuffle() return?\nWrite 'none' or 'array'"
            answer = "none"
            hint = "shuffle modifies the array directly and returns None"
        else:  # property
            question = "Which function creates a new randomly ordered array?\nWrite the function name (permutation or shuffle)"
            answer = "permutation"
            hint = "One returns a new array, the other modifies the original"
    elif difficulty == "medium":
        if question_type == "difference":
            array = np.array([1, 2, 3, 4, 5])
            question = f"Given: array = {array}\nWrite the code to create a shuffled copy without modifying the original"
            answer = "np.random.permutation(array)"
            hint = "If you want to keep the original unchanged, use the one that returns a new array"
        elif question_type == "use_case":
            question = "Write the code to shuffle an array in-place (modifies original, returns None)"
            answer = "np.random.shuffle(array)"
            hint = "shuffle modifies the array directly and returns None"
        elif question_type == "return":
            question = "What is the return type of np.random.permutation(array)?\nWrite 'array' or 'none'"
            answer = "array"
            hint = "permutation returns a new array, it doesn't modify the original"
        else:  # property
            array = np.random.randint(0, 15, size=random.randint(5, 10))
            question = f"Given: array = {array}\nWrite the code to randomly reorder it without creating a copy"
            answer = "np.random.shuffle(array)"
            hint = "shuffle modifies the array in-place, unlike permutation"
    else:  # hard
        question_type = random.choice(["difference", "use_case", "return", "property", "memory", "chain", "error"])
        if question_type == "difference":
            if random.choice([True, False]):
                question = "Write the code to shuffle an array in-place (modifies original, returns None)"
                answer = "np.random.shuffle(array)"
            else:
                question = "Write the code to create a shuffled copy without modifying the original"
                answer = "np.random.permutation(array)"
            hint = "One modifies in-place, the other returns a new array"
        elif question_type == "use_case":
            scenario = random.choice(["preserve", "memory", "multiple"])
            if scenario == "preserve":
                array = np.random.randint(0, 20, size=random.randint(8, 12))
                question = f"Given: array = {array}\nYou need both the original and shuffled version. Write the code to get shuffled copy"
                answer = "np.random.permutation(array)"
            elif scenario == "memory":
                question = "You have limited memory and want to shuffle a large array. Write the code (use in-place operation)"
                answer = "np.random.shuffle(array)"
            else:  # multiple
                question = "You need 3 different shuffled versions of the same array. Write the code for one shuffle (use function that returns new array)"
                answer = "np.random.permutation(array)"
            hint = "Consider whether you need the original array preserved"
        elif question_type == "return":
            if random.choice([True, False]):
                question = "What does np.random.shuffle(array) return?\nWrite 'none' or 'array'"
                answer = "none"
            else:
                question = "What does np.random.permutation(array) return?\nWrite 'none' or 'array'"
                answer = "array"
            hint = "One returns None, the other returns a new array"
        elif question_type == "property":
            question = "Write the code to randomly rearrange an array and get a new array back"
            answer = "np.random.permutation(array)"
            hint = "permutation returns a new array, it doesn't modify the original"
        elif question_type == "memory":
            question = "Which function is better for memory-constrained environments when shuffling large arrays?\nWrite the function name (permutation or shuffle)"
            answer = "shuffle"
            hint = "In-place operations don't create copies"
        elif question_type == "chain":
            question = "You want to chain operations: shuffled = shuffle(array) and then use shuffled. Which function allows this?\nWrite the function name (permutation or shuffle)"
            answer = "permutation"
            hint = "You need a function that returns a value to chain operations"
        else:  # error
            question = "If you try to assign result = np.random.shuffle(array), what will result be?\nWrite 'none' or 'array'"
            answer = "none"
            hint = "shuffle returns None, so assignment won't work as expected"
    
    return {"type": "comparison", "question": question, "answer": answer, "hint": hint}


def generate_random_array_challenge(difficulty="easy"):
    """Generate challenge for creating random arrays"""
    question_type = random.choice(["random", "uniform", "seed"])
    
    if difficulty == "easy":
        if question_type == "random":
            size = random.randint(5, 10)
            question = f"Write the code to generate an array of {size} random floats between 0 and 1"
            answer = f"np.random.random({size})"
        elif question_type == "uniform":
            size = random.randint(5, 8)
            low = random.randint(1, 5)
            high = random.randint(6, 10)
            question = f"Write the code to generate {size} random floats between {low} and {high}"
            answer = f"np.random.uniform({low}, {high}, size={size})"
        else:  # seed
            question = "Write the code to set the random seed to 42 for reproducibility"
            answer = "np.random.seed(42)"
        hint = "What function generates random floats in [0, 1)?"
    elif difficulty == "medium":
        if question_type == "random":
            shape = (random.randint(3, 5), random.randint(3, 5))
            question = f"Write the code to generate a 2D array with shape {shape} of random floats between 0 and 1"
            answer = f"np.random.random({shape})"
        elif question_type == "uniform":
            shape = (random.randint(3, 5), random.randint(3, 5))
            low = random.randint(0, 5)
            high = random.randint(6, 15)
            question = f"Write the code to generate a 2D array with shape {shape} of random floats between {low} and {high}"
            answer = f"np.random.uniform({low}, {high}, size={shape})"
        else:  # seed
            seed = random.randint(0, 100)
            question = f"Write the code to set the random number generator seed to {seed}"
            answer = f"np.random.seed({seed})"
        hint = "random() can take a shape tuple for multi-dimensional arrays"
    else:  # hard
        if question_type == "random":
            shape = (random.randint(3, 5), random.randint(3, 5), random.randint(2, 3))
            question = f"Write the code to generate a 3D array with shape {shape} of random floats between 0 and 1"
            answer = f"np.random.random({shape})"
        elif question_type == "uniform":
            low = random.randint(1, 10)
            high = random.randint(11, 30)
            shape = (random.randint(3, 5), random.randint(3, 5))
            question = f"Write the code to generate a 2D array with shape {shape} of random floats between {low} and {high}"
            answer = f"np.random.uniform({low}, {high}, size={shape})"
        else:  # seed
            seed = random.randint(0, 1000)
            question = f"Write the code to initialize the random number generator with seed {seed}"
            answer = f"np.random.seed({seed})"
        hint = "uniform() generates random floats in a specified range"
    
    return {"type": "random_array", "question": question, "answer": answer, "hint": hint}


def generate_true_false_challenge(difficulty="easy"):
    """Generate true/false questions about random operations"""
    question_type = random.choice([
        "permutation", "shuffle", "choice", "randint", "random", 
        "seed", "comparison", "return", "inplace", "distribution"
    ])
    
    if difficulty == "easy":
        if question_type == "permutation":
            question = "True or False: np.random.permutation(array) returns a new array without modifying the original."
            answer = "true"
        elif question_type == "shuffle":
            question = "True or False: np.random.shuffle(array) modifies the array in-place and returns None."
            answer = "true"
        elif question_type == "choice":
            question = "True or False: np.random.choice(array) randomly selects one element from the array."
            answer = "true"
        elif question_type == "randint":
            question = "True or False: np.random.randint(0, 10) generates a random integer from 0 to 10 (inclusive)."
            answer = "false"
        else:  # random
            question = "True or False: np.random.random(5) generates 5 random floats between 0 and 1."
            answer = "true"
        hint = "Think about how NumPy random functions work"
    elif difficulty == "medium":
        if question_type == "permutation":
            question = "True or False: np.random.permutation(10) creates a random permutation of integers 0-9."
            answer = "true"
        elif question_type == "shuffle":
            question = "True or False: You can assign the result of np.random.shuffle(array) to a variable."
            answer = "false"
        elif question_type == "choice":
            question = "True or False: np.random.choice(array, size=3) selects 3 elements with replacement by default."
            answer = "true"
        elif question_type == "randint":
            question = "True or False: np.random.randint(5, 15, size=(3, 4)) creates a 3x4 array of random integers."
            answer = "true"
        elif question_type == "random":
            question = "True or False: np.random.random((2, 3)) generates a 2D array with shape (2, 3)."
            answer = "true"
        elif question_type == "seed":
            question = "True or False: Setting the same seed value guarantees the same random sequence."
            answer = "true"
        elif question_type == "comparison":
            question = "True or False: permutation() and shuffle() produce the same result but work differently."
            answer = "true"
        elif question_type == "return":
            question = "True or False: Both permutation() and shuffle() return a new array."
            answer = "false"
        else:  # distribution
            question = "True or False: np.random.randint(0, 10) can generate the value 10."
            answer = "false"
        hint = "Consider the behavior and return values of random functions"
    else:  # hard
        if question_type == "permutation":
            question = "True or False: np.random.permutation() can work with multi-dimensional arrays."
            answer = "true"
        elif question_type == "shuffle":
            question = "True or False: np.random.shuffle() works along the first axis for 2D arrays."
            answer = "true"
        elif question_type == "choice":
            question = "True or False: np.random.choice(array, size=5, replace=False) requires the array to have at least 5 elements."
            answer = "true"
        elif question_type == "randint":
            question = "True or False: np.random.randint(-10, 10) can generate negative integers."
            answer = "true"
        elif question_type == "random":
            question = "True or False: np.random.random() generates values in the range [0, 1) (0 inclusive, 1 exclusive)."
            answer = "true"
        elif question_type == "seed":
            question = "True or False: Setting a seed only affects the next random operation, not subsequent ones."
            answer = "false"
        elif question_type == "comparison":
            question = "True or False: For memory efficiency with large arrays, shuffle() is better than permutation()."
            answer = "true"
        elif question_type == "return":
            question = "True or False: permutation() always returns a copy, never a view."
            answer = "true"
        elif question_type == "inplace":
            question = "True or False: shuffle() is an in-place operation that modifies the original array."
            answer = "true"
        else:  # distribution
            question = "True or False: np.random.uniform(1, 10, size=5) generates 5 floats between 1 and 10 (inclusive)."
            answer = "true"
        hint = "Advanced random operations require understanding memory and behavior"
    
    return {"type": "true_false", "question": question, "answer": answer, "hint": hint}


def validate_code_answer(user_input, correct_answer):
    """
    Validate user's code answer.
    Normalizes whitespace and handles variations in code formatting.
    Also handles function names and simple string answers.
    """
    def normalize_code(code):
        # Remove all whitespace
        code = ''.join(code.split())
        # Convert to lowercase for case-insensitive comparison
        return code.lower()
    
    user_normalized = normalize_code(user_input)
    correct_normalized = normalize_code(correct_answer)
    
    # Handle simple string answers (e.g., "permutation", "shuffle", "none", "array")
    if correct_normalized in ["permutation", "shuffle", "none", "array"]:
        # Direct match
        if user_normalized == correct_normalized:
            return True
        # For function names, also accept full path
        if correct_normalized in ["permutation", "shuffle"]:
            if user_normalized == f"np.random.{correct_normalized}" or user_normalized.endswith(f".{correct_normalized}"):
                return True
        return False
    
    # For code answers, do exact normalized comparison
    return user_normalized == correct_normalized


def show_hint(challenge):
    """Display a hint for the current challenge."""
    print(f"Hint: {challenge['hint']}")


def play_game():
    """
    Run a single game session.
    """
    print("Welcome to Vector Battle!")
    print("Master NumPy random operations and permutations!\n")
    
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
    
    # Determine number of T/F questions
    if difficulty == "easy":
        tf_count = 1
        code_count = 5
    elif difficulty == "medium":
        tf_count = 3
        code_count = 10
    else:  # hard
        tf_count = 5
        code_count = 15
    
    # Challenge functions
    challenge_functions = [
        generate_permutation_challenge,
        generate_shuffle_challenge,
        generate_distribution_challenge,
        generate_choice_challenge,
        generate_comparison_challenge,
        generate_random_array_challenge
    ]
    
    # Create challenge sequence with diversity
    challenge_sequence = []
    for _ in range(code_count):
        challenge_sequence.append(random.choice(challenge_functions))
    
    # Add T/F questions
    for _ in range(tf_count):
        challenge_sequence.append(generate_true_false_challenge)
    
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
        print("Perfect score! You're a random operations master! 🎉")
    elif percentage >= 80:
        print("Excellent work! You're getting really good! 🌟")
    elif percentage >= 60:
        print("Good job! Keep practicing! 👍")
    else:
        print("Keep practicing! You'll get better! 💪")
    
    print("\nThank you for playing Vector Battle!")


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