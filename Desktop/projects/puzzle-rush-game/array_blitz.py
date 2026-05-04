import numpy as np
import random

"""
Array Blitz - A fast-paced NumPy array manipulation game

This game challenges you to:
- Create arrays
- Manipulate arrays (indexing, slicing)
- Transform arrays (reshape, join, split)
- Search and sort arrays
- Filter arrays
"""     

def generate_create_challenge(difficulty="easy"):
    if difficulty == "easy":
        start = random.randint(0, 5)
        stop = random.randint(6, 15)
        step = random.randint(1, 3)
    elif difficulty == "medium":
        start = random.randint(-5, 10)
        stop = random.randint(11, 30)
        step = random.randint(1, 5)
    else:  # hard
        start = random.randint(-20, 10)
        stop = random.randint(11, 50)
        step = random.randint(2, 7)
    
    question = f"Write the code to create an array of numbers from {start} to {stop} with a step of {step}"
    answer = f"np.arange({start}, {stop}, {step})"  # Code as answer
    hint = "NumPy has functions for generating arrays. What creates sequences?"
    return {"type": "create", "question": question, "answer": answer, "hint": hint}


def generate_shape_challenge(difficulty="easy"):
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=(random.randint(2, 5), random.randint(2, 5)))
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=(random.randint(3, 8), random.randint(3, 8)))
    else:  # hard
        # Hard: 3D arrays or larger 2D arrays
        if random.choice([True, False]):
            array = np.random.randint(0, 50, size=(random.randint(5, 10), random.randint(5, 10)))
        else:
            array = np.random.randint(0, 50, size=(random.randint(2, 5), random.randint(2, 5), random.randint(2, 4)))
    
    question = f"Given: array = \n{array}\nWrite the code to get its shape"
    answer = "array.shape"  # Code as answer
    hint = "What describes how many elements are in each dimension?"
    return {"type": "shape", "question": question, "answer": answer, "hint": hint}


def generate_reshape_challenge(difficulty="easy"):
    # Generate array and ensure valid reshape
    while True:
        if difficulty == "easy":
            array = np.random.randint(0, 10, size=(random.randint(2, 4), random.randint(2, 4)))
            new_shape = (random.randint(2, 4), random.randint(2, 4))
        elif difficulty == "medium":
            array = np.random.randint(0, 20, size=(random.randint(3, 6), random.randint(3, 6)))
            new_shape = (random.randint(3, 6), random.randint(3, 6))
        else:  # hard
            # Hard: 3D reshape or larger 2D
            if random.choice([True, False]):
                array = np.random.randint(0, 50, size=(random.randint(4, 8), random.randint(4, 8)))
                new_shape = (random.randint(4, 8), random.randint(4, 8))
            else:
                array = np.random.randint(0, 50, size=(random.randint(2, 4), random.randint(2, 4), random.randint(2, 4)))
                new_shape = (random.randint(2, 4), random.randint(2, 4), random.randint(2, 4))
        
        # Validate that the reshape is possible
        if array.size == np.prod(new_shape):
            break
    
    question = f"Given: array = \n{array}\nWrite the code to reshape it to {new_shape}"
    # Format the answer with proper tuple syntax
    if len(new_shape) == 2:
        answer = f"array.reshape(({new_shape[0]}, {new_shape[1]}))"
    else:  # 3D
        answer = f"array.reshape(({new_shape[0]}, {new_shape[1]}, {new_shape[2]}))"
    hint = "The total number of elements must stay the same"
    return {"type": "reshape", "question": question, "answer": answer, "hint": hint}


def generate_slice_challenge(difficulty="easy"):
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=random.randint(5, 10))
        start = random.randint(0, len(array) - 3)
        stop = random.randint(start + 1, len(array))
        question = f"Given: array = {array}\nWrite the code to slice it from index {start} to {stop} (exclusive)"
        answer = f"array[{start}:{stop}]"  # Code as answer
        hint = "How do you extract a portion of a sequence in Python?"
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=random.randint(10, 20))
        start = random.randint(0, len(array) - 5)
        stop = random.randint(start + 2, len(array))
        step = random.choice([1, 2])  # Add step slicing
        question = f"Given: array = {array}\nWrite the code to slice it from index {start} to {stop} with step {step} (exclusive)"
        answer = f"array[{start}:{stop}:{step}]"  # Code as answer
        hint = "You can add a third parameter to control how elements are selected"
    else:  # hard
        array = np.random.randint(0, 50, size=random.randint(15, 30))
        start = random.randint(0, len(array) - 8)
        stop = random.randint(start + 3, len(array))
        step = random.choice([1, 2, 3])
        # Hard: negative indexing or complex slicing
        if random.choice([True, False]):
            question = f"Given: array = {array}\nWrite the code to slice it from index {start} to {stop} with step {step} (exclusive)"
            answer = f"array[{start}:{stop}:{step}]"  # Code as answer
            hint = "The middle number determines where to stop, but doesn't include that element"
        else:
            # Negative indexing
            neg_stop = -random.randint(1, len(array) - stop)
            question = f"Given: array = {array}\nWrite the code to slice it from index {start} to {neg_stop} (using negative index)"
            answer = f"array[{start}:{neg_stop}]"  # Code as answer
            hint = "What happens when you use negative numbers as indices?"
    
    return {"type": "slice", "question": question, "answer": answer, "hint": hint}

def generate_filter_challenge(difficulty="easy"):
    if difficulty == "easy":
        array = np.random.randint(0, 20, size=random.randint(5, 10))
        threshold = random.randint(5, 15)
        question = f"Given: array = {array}\nWrite the code to filter it to show only elements greater than {threshold}"
        answer = f"array[array > {threshold}]"  # Code with actual threshold value
        hint = "You can use boolean conditions inside square brackets to select elements"
    elif difficulty == "medium":
        array = np.random.randint(0, 50, size=random.randint(10, 20))
        threshold = random.randint(10, 40)
        # Medium: multiple conditions
        condition = random.choice(["greater", "less", "equal"])
        if condition == "greater":
            question = f"Given: array = {array}\nWrite the code to filter it to show only elements greater than {threshold}"
            answer = f"array[array > {threshold}]"
            hint = "Boolean indexing: create a condition and use it to index the array"
        elif condition == "less":
            question = f"Given: array = {array}\nWrite the code to filter it to show only elements less than {threshold}"
            answer = f"array[array < {threshold}]"
            hint = "The comparison operator creates a boolean array that selects elements"
        else:
            question = f"Given: array = {array}\nWrite the code to filter it to show only elements equal to {threshold}"
            answer = f"array[array == {threshold}]"
            hint = "How do you check if values are equal in Python?"
    else:  # hard
        array = np.random.randint(-20, 50, size=random.randint(15, 30))
        threshold1 = random.randint(-10, 30)
        threshold2 = random.randint(threshold1 + 5, 40)
        # Hard: range conditions or multiple conditions
        if random.choice([True, False]):
            question = f"Given: array = {array}\nWrite the code to filter it to show only elements between {threshold1} and {threshold2} (inclusive)"
            answer = f"array[(array >= {threshold1}) & (array <= {threshold2})]"
            hint = "How do you combine two boolean conditions in Python? (Hint: not 'and' or 'or')"
        else:
            # Even/odd filtering
            question = f"Given: array = {array}\nWrite the code to filter it to show only even elements"
            answer = "array[array % 2 == 0]"
            hint = "What mathematical operation tells you if a number is divisible by 2?"
    
    return {"type": "filter", "question": question, "answer": answer, "hint": hint}


def generate_sum_challenge(difficulty="easy"):
    """Generate challenge for np.sum()"""
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=random.randint(5, 10))
        question = f"Given: array = {array}\nWrite the code to calculate the sum of all elements"
        answer = "np.sum(array)"
        hint = "What function adds up all elements in an array?"
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=(random.randint(3, 6), random.randint(3, 6)))
        axis = random.choice([0, 1])
        question = f"Given: array = \n{array}\nWrite the code to sum along axis {axis}"
        answer = f"np.sum(array, axis={axis})"
        hint = "You can specify which dimension to sum along"
    else:  # hard
        array = np.random.randint(0, 50, size=(random.randint(4, 8), random.randint(4, 8), random.randint(2, 4)))
        axis = random.choice([0, 1, 2])
        question = f"Given: array = \n{array}\nWrite the code to sum along axis {axis}"
        answer = f"np.sum(array, axis={axis})"
        hint = "For 3D arrays, axis can be 0, 1, or 2"
    return {"type": "sum", "question": question, "answer": answer, "hint": hint}


def generate_search_challenge(difficulty="easy"):
    """Generate challenge for searching in arrays (np.where, np.argwhere)"""
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=random.randint(5, 10))
        value = random.choice(array.tolist())
        question = f"Given: array = {array}\nWrite the code to find indices where elements equal {value}"
        answer = f"np.where(array == {value})"
        hint = "What function finds positions based on a condition?"
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=random.randint(10, 15))
        value = random.randint(5, 15)
        question = f"Given: array = {array}\nWrite the code to find indices where elements are greater than {value}"
        answer = f"np.where(array > {value})"
        hint = "np.where returns indices where the condition is True"
    else:  # hard
        array = np.random.randint(0, 50, size=(random.randint(4, 6), random.randint(4, 6)))
        value = random.randint(10, 40)
        question = f"Given: array = \n{array}\nWrite the code to find indices where elements equal {value}"
        answer = f"np.argwhere(array == {value})"
        hint = "np.argwhere returns indices in a different format for 2D arrays"
    return {"type": "search", "question": question, "answer": answer, "hint": hint}


def generate_concatenate_challenge(difficulty="easy"):
    """Generate challenge for np.concatenate()"""
    if difficulty == "easy":
        arr1 = np.random.randint(0, 10, size=random.randint(3, 5))
        arr2 = np.random.randint(0, 10, size=random.randint(3, 5))
        question = f"Given: arr1 = {arr1}, arr2 = {arr2}\nWrite the code to concatenate them"
        answer = "np.concatenate([arr1, arr2])"
        hint = "What function joins arrays together?"
    elif difficulty == "medium":
        arr1 = np.random.randint(0, 20, size=(random.randint(2, 4), random.randint(2, 4)))
        arr2 = np.random.randint(0, 20, size=(random.randint(2, 4), random.randint(2, 4)))
        axis = random.choice([0, 1])
        question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}\nWrite the code to concatenate along axis {axis}"
        answer = f"np.concatenate([arr1, arr2], axis={axis})"
        hint = "You can specify which axis to concatenate along"
    else:  # hard
        arr1 = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        arr2 = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        arr3 = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        axis = random.choice([0, 1])
        question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}, arr3 = \n{arr3}\nWrite the code to concatenate all three along axis {axis}"
        answer = f"np.concatenate([arr1, arr2, arr3], axis={axis})"
        hint = "You can concatenate multiple arrays at once"
    return {"type": "concatenate", "question": question, "answer": answer, "hint": hint}


def generate_array_creation_challenge(difficulty="easy"):
    """Generate challenge for array creation (zeros, ones, full, etc.)"""
    creation_type = random.choice(["zeros", "ones", "full", "empty"])
    
    if difficulty == "easy":
        size = random.randint(3, 8)
        if creation_type == "zeros":
            question = f"Write the code to create an array of zeros with shape ({size},)"
            answer = f"np.zeros({size})"
            hint = "What function creates an array filled with zeros?"
        elif creation_type == "ones":
            question = f"Write the code to create an array of ones with shape ({size},)"
            answer = f"np.ones({size})"
            hint = "What function creates an array filled with ones?"
        elif creation_type == "full":
            value = random.randint(1, 10)
            question = f"Write the code to create an array of shape ({size},) filled with {value}"
            answer = f"np.full({size}, {value})"
            hint = "What function creates an array filled with a specific value?"
        else:  # empty
            question = f"Write the code to create an uninitialized array with shape ({size},)"
            answer = f"np.empty({size})"
            hint = "What function creates an array without initializing values?"
    elif difficulty == "medium":
        shape = (random.randint(3, 6), random.randint(3, 6))
        if creation_type == "zeros":
            question = f"Write the code to create a 2D array of zeros with shape {shape}"
            answer = f"np.zeros({shape})"
            hint = "The shape parameter should be a tuple"
        elif creation_type == "ones":
            question = f"Write the code to create a 2D array of ones with shape {shape}"
            answer = f"np.ones({shape})"
            hint = "For 2D arrays, use a tuple for the shape"
        elif creation_type == "full":
            value = random.randint(1, 20)
            question = f"Write the code to create a 2D array with shape {shape} filled with {value}"
            answer = f"np.full({shape}, {value})"
            hint = "np.full takes shape and fill value as parameters"
        else:  # empty
            question = f"Write the code to create an uninitialized 2D array with shape {shape}"
            answer = f"np.empty({shape})"
            hint = "np.empty creates arrays without initialization"
    else:  # hard
        shape = (random.randint(3, 5), random.randint(3, 5), random.randint(2, 4))
        if creation_type == "zeros":
            question = f"Write the code to create a 3D array of zeros with shape {shape}"
            answer = f"np.zeros({shape})"
            hint = "3D arrays use a 3-element tuple for shape"
        elif creation_type == "ones":
            question = f"Write the code to create a 3D array of ones with shape {shape}"
            answer = f"np.ones({shape})"
            hint = "The shape tuple determines all dimensions"
        elif creation_type == "full":
            value = random.randint(1, 50)
            question = f"Write the code to create a 3D array with shape {shape} filled with {value}"
            answer = f"np.full({shape}, {value})"
            hint = "np.full works with any number of dimensions"
        else:  # empty
            question = f"Write the code to create an uninitialized 3D array with shape {shape}"
            answer = f"np.empty({shape})"
            hint = "np.empty can create arrays of any shape"
    
    return {"type": "creation", "question": question, "answer": answer, "hint": hint}


def generate_copy_view_challenge(difficulty="easy"):
    """Generate challenge for copy vs view"""
    array = np.random.randint(0, 10, size=random.randint(5, 10))
    
    if difficulty == "easy":
        question = f"Given: array = {array}\nWrite the code to create a copy of the array"
        answer = "array.copy()"
        hint = "What method creates an independent copy?"
    elif difficulty == "medium":
        question = f"Given: array = {array}\nWrite the code to create a view of the array"
        answer = "array.view()"
        hint = "A view shares data with the original array"
    else:  # hard
        operation = random.choice(["copy", "view"])
        if operation == "copy":
            question = f"Given: array = {array}\nWrite the code to create a deep copy (independent copy)"
            answer = "np.copy(array)"
            hint = "np.copy() creates an independent copy"
        else:
            question = f"Given: array = {array}\nWrite the code to create a view (shares memory)"
            answer = "array.view()"
            hint = "Views share the same data buffer"
    
    return {"type": "copy_view", "question": question, "answer": answer, "hint": hint}


def generate_indexing_challenge(difficulty="easy"):
    """Generate challenge for array indexing"""
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=random.randint(5, 10))
        index = random.randint(0, len(array) - 1)
        question = f"Given: array = {array}\nWrite the code to access the element at index {index}"
        answer = f"array[{index}]"
        hint = "How do you access a specific element by position?"
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=(random.randint(3, 6), random.randint(3, 6)))
        row = random.randint(0, array.shape[0] - 1)
        col = random.randint(0, array.shape[1] - 1)
        question = f"Given: array = \n{array}\nWrite the code to access element at row {row}, column {col}"
        answer = f"array[{row}, {col}]"
        hint = "2D arrays use row, column indexing"
    else:  # hard
        array = np.random.randint(0, 50, size=(random.randint(2, 4), random.randint(2, 4), random.randint(2, 3)))
        indices = tuple(random.randint(0, array.shape[i] - 1) for i in range(3))
        question = f"Given: array = \n{array}\nWrite the code to access element at {indices}"
        answer = f"array[{indices[0]}, {indices[1]}, {indices[2]}]"
        hint = "3D arrays use three indices: depth, row, column"
    
    return {"type": "indexing", "question": question, "answer": answer, "hint": hint}


def generate_join_challenge(difficulty="easy"):
    """Generate challenge for joining arrays (stack, hstack, vstack)"""
    if difficulty == "easy":
        arr1 = np.random.randint(0, 10, size=random.randint(3, 5))
        arr2 = np.random.randint(0, 10, size=random.randint(3, 5))
        join_type = random.choice(["hstack", "vstack"])
        if join_type == "hstack":
            question = f"Given: arr1 = {arr1}, arr2 = {arr2}\nWrite the code to stack them horizontally"
            answer = "np.hstack([arr1, arr2])"
            hint = "hstack joins arrays horizontally (side by side)"
        else:
            question = f"Given: arr1 = {arr1}, arr2 = {arr2}\nWrite the code to stack them vertically"
            answer = "np.vstack([arr1, arr2])"
            hint = "vstack joins arrays vertically (on top of each other)"
    elif difficulty == "medium":
        arr1 = np.random.randint(0, 20, size=(random.randint(2, 4), random.randint(2, 4)))
        arr2 = np.random.randint(0, 20, size=(random.randint(2, 4), random.randint(2, 4)))
        join_type = random.choice(["hstack", "vstack", "stack"])
        if join_type == "hstack":
            question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}\nWrite the code to stack them horizontally"
            answer = "np.hstack([arr1, arr2])"
            hint = "hstack concatenates along the second axis"
        elif join_type == "vstack":
            question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}\nWrite the code to stack them vertically"
            answer = "np.vstack([arr1, arr2])"
            hint = "vstack concatenates along the first axis"
        else:
            axis = random.choice([0, 1])
            question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}\nWrite the code to stack them along axis {axis}"
            answer = f"np.stack([arr1, arr2], axis={axis})"
            hint = "np.stack creates a new axis"
    else:  # hard
        arr1 = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        arr2 = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        arr3 = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
        join_type = random.choice(["hstack", "vstack", "stack"])
        if join_type == "hstack":
            question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}, arr3 = \n{arr3}\nWrite the code to stack all three horizontally"
            answer = "np.hstack([arr1, arr2, arr3])"
            hint = "hstack can join multiple arrays"
        elif join_type == "vstack":
            question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}, arr3 = \n{arr3}\nWrite the code to stack all three vertically"
            answer = "np.vstack([arr1, arr2, arr3])"
            hint = "vstack can join multiple arrays"
        else:
            axis = random.choice([0, 1, 2])
            question = f"Given: arr1 = \n{arr1}, arr2 = \n{arr2}, arr3 = \n{arr3}\nWrite the code to stack them along axis {axis}"
            answer = f"np.stack([arr1, arr2, arr3], axis={axis})"
            hint = "np.stack adds a new dimension"
    
    return {"type": "join", "question": question, "answer": answer, "hint": hint}


def generate_split_challenge(difficulty="easy"):
    """Generate challenge for splitting arrays"""
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=random.randint(6, 12))
        num_splits = random.choice([2, 3])
        question = f"Given: array = {array}\nWrite the code to split it into {num_splits} equal parts"
        answer = f"np.split(array, {num_splits})"
        hint = "What function divides an array into multiple parts?"
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=random.randint(10, 15))
        indices = sorted(random.sample(range(1, len(array)), 2))
        question = f"Given: array = {array}\nWrite the code to split at indices {indices}"
        answer = f"np.split(array, {indices})"
        hint = "You can specify where to split using indices"
    else:  # hard
        array = np.random.randint(0, 50, size=(random.randint(4, 6), random.randint(4, 6)))
        axis = random.choice([0, 1])
        num_splits = random.choice([2, 3])
        question = f"Given: array = \n{array}\nWrite the code to split along axis {axis} into {num_splits} parts"
        answer = f"np.split(array, {num_splits}, axis={axis})"
        hint = "You can split along different axes for 2D arrays"
    
    return {"type": "split", "question": question, "answer": answer, "hint": hint}


def generate_sort_challenge(difficulty="easy"):
    """Generate challenge for sorting arrays"""
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=random.randint(5, 10))
        question = f"Given: array = {array}\nWrite the code to sort the array"
        answer = "np.sort(array)"
        hint = "What function arranges elements in order?"
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=(random.randint(3, 6), random.randint(3, 6)))
        axis = random.choice([0, 1, None])
        if axis is None:
            question = f"Given: array = \n{array}\nWrite the code to sort all elements"
            answer = "np.sort(array, axis=None)"
            hint = "axis=None flattens the array before sorting"
        else:
            question = f"Given: array = \n{array}\nWrite the code to sort along axis {axis}"
            answer = f"np.sort(array, axis={axis})"
            hint = "You can sort along specific axes"
    else:  # hard
        array = np.random.randint(0, 50, size=random.randint(10, 20))
        kind = random.choice(["quicksort", "mergesort", "heapsort"])
        question = f"Given: array = {array}\nWrite the code to sort using {kind} algorithm"
        answer = f"np.sort(array, kind='{kind}')"
        hint = "NumPy supports different sorting algorithms"
    
    return {"type": "sort", "question": question, "answer": answer, "hint": hint}


def generate_permutation_challenge(difficulty="easy"):
    """Generate challenge for permutation and shuffling"""
    if difficulty == "easy":
        array = np.random.randint(0, 10, size=random.randint(5, 10))
        question = f"Given: array = {array}\nWrite the code to create a random permutation of the array"
        answer = "np.random.permutation(array)"
        hint = "What function randomly rearranges elements?"
    elif difficulty == "medium":
        array = np.random.randint(0, 20, size=random.randint(8, 12))
        question = f"Given: array = {array}\nWrite the code to shuffle the array in-place"
        answer = "np.random.shuffle(array)"
        hint = "shuffle modifies the array directly, unlike permutation"
    else:  # hard
        size = random.randint(10, 20)
        question = f"Write the code to create a random permutation of integers from 0 to {size-1}"
        answer = f"np.random.permutation({size})"
        hint = "permutation can take an integer to permute a range"
    
    return {"type": "permutation", "question": question, "answer": answer, "hint": hint}


def validate_array_answer(user_input, correct_answer):
    """
    Validate user's array answer.
    User input is expected to be a string that can be parsed as a list/array.
    """
    try:
        # Parse string input like "[1, 2, 3]" or "1, 2, 3"
        user_input = user_input.strip()
        if user_input.startswith('[') and user_input.endswith(']'):
            user_input = user_input[1:-1]
        # Convert to list then numpy array
        user_array = np.array([int(x.strip()) for x in user_input.split(',')])
        return np.array_equal(user_array, correct_answer)
    except (ValueError, AttributeError):
        return False


def generate_true_false_challenge(difficulty="easy"):
    """Generate true/false questions about array operations"""
    question_type = random.choice([
        "reshape", "copy_view", "slicing", "filtering", "sorting", 
        "concatenation", "searching", "indexing", "shape", "creation"
    ])
    
    if difficulty == "easy":
        if question_type == "reshape":
            question = "True or False: Reshaping an array changes the total number of elements."
            answer = "false"
        elif question_type == "copy_view":
            question = "True or False: array.copy() creates a deep copy that is independent of the original."
            answer = "true"
        elif question_type == "slicing":
            question = "True or False: Slicing an array (e.g., array[1:3]) creates a view, not a copy."
            answer = "true"
        elif question_type == "filtering":
            question = "True or False: array[array > 5] returns a new array with elements greater than 5."
            answer = "true"
        else:  # shape
            question = "True or False: The shape of a 1D array with 10 elements is (10, 1)."
            answer = "false"
        hint = "Think about how NumPy handles array operations"
    elif difficulty == "medium":
        if question_type == "reshape":
            question = "True or False: You can reshape a (3, 4) array to (2, 6) because both have 12 elements."
            answer = "true"
        elif question_type == "copy_view":
            question = "True or False: Modifying a view of an array will also modify the original array."
            answer = "true"
        elif question_type == "slicing":
            question = "True or False: array[::-1] reverses the array."
            answer = "true"
        elif question_type == "filtering":
            question = "True or False: Boolean indexing (array[array > 5]) returns a copy, not a view."
            answer = "true"
        elif question_type == "sorting":
            question = "True or False: np.sort(array) modifies the original array in-place."
            answer = "false"
        elif question_type == "concatenation":
            question = "True or False: np.concatenate() can join arrays along any axis."
            answer = "true"
        elif question_type == "searching":
            question = "True or False: np.where(array == 5) returns the indices where the condition is True."
            answer = "true"
        elif question_type == "indexing":
            question = "True or False: array[0] and array[0, :] are equivalent for a 2D array."
            answer = "false"
        else:  # shape
            question = "True or False: A 2D array with shape (3, 4) has 7 elements total."
            answer = "false"
        hint = "Consider how NumPy operations work internally"
    else:  # hard
        if question_type == "reshape":
            question = "True or False: You can use -1 in reshape to automatically calculate one dimension."
            answer = "true"
        elif question_type == "copy_view":
            question = "True or False: array.view() creates a new array object that shares the same data buffer."
            answer = "true"
        elif question_type == "slicing":
            question = "True or False: array[::2] selects every other element starting from index 0."
            answer = "true"
        elif question_type == "filtering":
            question = "True or False: Multiple conditions can be combined with & (and) or | (or) for boolean indexing."
            answer = "true"
        elif question_type == "sorting":
            question = "True or False: array.sort() sorts the array in-place and returns None."
            answer = "true"
        elif question_type == "concatenation":
            question = "True or False: np.concatenate() requires arrays to have the same shape along all axes except the concatenation axis."
            answer = "true"
        elif question_type == "searching":
            question = "True or False: np.argmax(array) returns the index of the maximum value."
            answer = "true"
        elif question_type == "indexing":
            question = "True or False: Fancy indexing (array[[0, 2, 4]]) always returns a copy."
            answer = "true"
        elif question_type == "shape":
            question = "True or False: A 3D array with shape (2, 3, 4) has 24 elements total."
            answer = "true"
        else:  # creation
            question = "True or False: np.arange(0, 10, 2) creates an array [0, 2, 4, 6, 8]."
            answer = "true"
        hint = "Advanced NumPy concepts require understanding memory layout and operations"
    
    return {"type": "true_false", "question": question, "answer": answer, "hint": hint}


def validate_code_answer(user_input, correct_answer):
    """
    Validate user's code answer.
    Normalizes whitespace and handles variations in code formatting.
    """
    # Normalize both strings: remove extra whitespace, convert to lowercase
    def normalize_code(code):
        # Remove all whitespace
        code = ''.join(code.split())
        # Convert to lowercase for case-insensitive comparison
        return code.lower()
    
    user_normalized = normalize_code(user_input)
    correct_normalized = normalize_code(correct_answer)
    
    return user_normalized == correct_normalized


def show_hint(challenge):
    print(f"Hint: {challenge['hint']}")


def play_game():
    """
    Run a single game session.
    """
    print("Welcome to Array Blitz! The game that will test your manipulation skills... On arrays, of course :)")
    print("Test your NumPy array manipulation skills!\n")
    
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
    
    # Challenge functions (excluding shape - it will be added once)
    other_challenge_functions = [
        generate_create_challenge,
        generate_reshape_challenge,
        generate_slice_challenge,
        generate_filter_challenge,
        generate_sum_challenge,
        generate_search_challenge,
        generate_concatenate_challenge,
        generate_array_creation_challenge,
        generate_copy_view_challenge,
        generate_indexing_challenge,
        generate_join_challenge,
        generate_split_challenge,
        generate_sort_challenge,
        generate_permutation_challenge
    ]
    
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
    
    # Create challenge sequence: ensure shape appears exactly once
    # Fill code challenge slots with other challenge types for diversity
    challenge_sequence = [generate_shape_challenge]  # Shape appears once
    
    # Fill the rest of code challenges
    remaining_code_slots = code_count - 1
    for _ in range(remaining_code_slots):
        challenge_sequence.append(random.choice(other_challenge_functions))
    
    # Add T/F questions
    for _ in range(tf_count):
        challenge_sequence.append(generate_true_false_challenge)
    
    # Shuffle to randomize order (shape will appear somewhere in the sequence)
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
        print("Perfect score! You're an array master! 🎉")
    elif percentage >= 80:
        print("Excellent work! You're getting really good! 🌟")
    elif percentage >= 60:
        print("Good job! Keep practicing! 👍")
    else:
        print("Keep practicing! You'll get better! 💪")
    
    print("\nThank you for playing Array Blitz!")


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