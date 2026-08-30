import numpy as np
import random
from exercise_session import run_standard_game
from session_common import EXERCISE_BACKGROUNDS, build_teach_body_lines, pick_true_false_statement
from hints import HINT_001, HINT_002, HINT_003, HINT_004, HINT_005, HINT_006, HINT_007, HINT_008, HINT_009, HINT_010, HINT_011, HINT_012, HINT_013, HINT_014, HINT_015, HINT_016, HINT_017, HINT_018, HINT_019, HINT_020
"""
Array Blitz - A fast-paced NumPy array manipulation game

This game challenges you to:
- Create arrays
- Manipulate arrays (indexing, slicing)
- Transform arrays (reshape, join, split)
- Search and sort arrays
- Filter arrays
"""


def generate_create_challenge():
    start = random.randint(-20, 10)
    stop = random.randint(11, 50)
    step = random.randint(2, 7)
    question = f'Write the code to create an array of numbers from {start} to {stop} with a step of {step}'
    answer = f'np.arange({start}, {stop}, {step})'
    hint = HINT_001
    return {'type': 'create', 'question': question, 'answer': answer, 'hint': hint}

def generate_shape_challenge():
    if random.choice([True, False]):
        array = np.random.randint(0, 50, size=(random.randint(5, 10), random.randint(5, 10)))
    else:
        array = np.random.randint(
            0, 50, size=(random.randint(2, 5), random.randint(2, 5), random.randint(2, 4))
        )
    question = f'Given the array a, write the code to get its shape'
    answer = 'a.shape'
    hint = HINT_002
    return {'type': 'shape', 'question': question, 'answer': answer, 'hint': hint}

def generate_reshape_challenge():
    while True:
        if random.choice([True, False]):
            array = np.random.randint(0, 50, size=(random.randint(4, 8), random.randint(4, 8)))
            new_shape = (random.randint(4, 8), random.randint(4, 8))
        else:
            array = np.random.randint(
                0, 50, size=(random.randint(2, 4), random.randint(2, 4), random.randint(2, 4))
            )
            new_shape = (random.randint(2, 4), random.randint(2, 4), random.randint(2, 4))
        if array.size == np.prod(new_shape):
            break
    question = f'Given the array a, write the code to reshape it to {new_shape}'
    if len(new_shape) == 2:
        answer = f'a.reshape(({new_shape[0]}, {new_shape[1]}))'
    else:
        answer = f'a.reshape(({new_shape[0]}, {new_shape[1]}, {new_shape[2]}))'
    hint = HINT_003
    return {'type': 'reshape', 'question': question, 'answer': answer, 'hint': hint}

def generate_slice_challenge():
    array = np.random.randint(0, 50, size=random.randint(15, 30))
    start = random.randint(0, len(array) - 8)
    stop = random.randint(start + 3, len(array))
    step = random.choice([1, 2, 3])
    if random.choice([True, False]):
        question = f'Given the array a, write the code to slice it from index {start} to {stop} with step {step} (exclusive)'
        answer = f'a[{start}:{stop}:{step}]'
        hint = HINT_012
    else:
        span = len(array) - stop
        if span <= 0:
            neg_stop = -1
        else:
            neg_stop = -random.randint(1, span)
        question = f'Given the array a, write the code to slice it from index {start} to {neg_stop} (using negative index)'
        answer = f'a[{start}:{neg_stop}]'
        hint = HINT_013
    return {'type': 'slice', 'question': question, 'answer': answer, 'hint': hint}

def generate_filter_challenge():
    array = np.random.randint(-20, 50, size=random.randint(15, 30))
    threshold1 = random.randint(-10, 30)
    threshold2 = random.randint(threshold1 + 5, 40)
    if random.choice([True, False]):
        question = f'Given the array a, write the code to filter it to show only elements between {threshold1} and {threshold2} (inclusive)'
        answer = f'a[(a >= {threshold1}) & (a <= {threshold2})]'
        hint = HINT_014
    else:
        question = f'Given the array a, write the code to filter it to show only even elements'
        answer = 'a[a % 2 == 0]'
        hint = HINT_015
    return {'type': 'filter', 'question': question, 'answer': answer, 'hint': hint}

def generate_sum_challenge():
    """Generate challenge for np.sum()"""
    array = np.random.randint(0, 50, size=(random.randint(4, 8), random.randint(4, 8), random.randint(2, 4)))
    axis = random.choice([0, 1, 2])
    question = f'Given the array a, write the code to sum along axis {axis}'
    answer = f'np.sum(a, axis={axis})'
    hint = HINT_004
    return {'type': 'sum', 'question': question, 'answer': answer, 'hint': hint}

def generate_search_challenge():
    """Generate challenge for searching in arrays (np.where, np.argwhere)"""
    array = np.random.randint(0, 50, size=(random.randint(4, 6), random.randint(4, 6)))
    value = random.randint(10, 40)
    question = f'Given the array a, write the code to find indices where elements equal {value}'
    answer = f'np.argwhere(a == {value})'
    hint = HINT_005
    return {'type': 'search', 'question': question, 'answer': answer, 'hint': hint}

def generate_concatenate_challenge():
    """Generate challenge for np.concatenate()"""
    a = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
    b = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
    c = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
    axis = random.choice([0, 1])
    question = f'Given the arrays a, b, and c, write the code to concatenate all three along axis {axis}'
    answer = f'np.concatenate([a, b, c], axis={axis})'
    hint = HINT_006
    return {'type': 'concatenate', 'question': question, 'answer': answer, 'hint': hint}

def generate_array_creation_challenge():
    """Generate challenge for array creation (zeros, ones, full, etc.)"""
    creation_type = random.choice(['zeros', 'ones', 'full', 'empty'])
    shape = (random.randint(3, 5), random.randint(3, 5), random.randint(2, 4))
    creation_hint = HINT_007
    if creation_type == 'zeros':
        question = f'Write the code to create a 3D array of zeros with shape {shape}'
        answer = f'np.zeros({shape})'
        hint = creation_hint
    elif creation_type == 'ones':
        question = f'Write the code to create a 3D array of ones with shape {shape}'
        answer = f'np.ones({shape})'
        hint = creation_hint
    elif creation_type == 'full':
        value = random.randint(1, 50)
        question = f'Write the code to create a 3D array with shape {shape} filled with {value}'
        answer = f'np.full({shape}, {value})'
        hint = creation_hint
    else:
        question = f'Write the code to create an uninitialized 3D array with shape {shape}'
        answer = f'np.empty({shape})'
        hint = creation_hint
    return {'type': 'creation', 'question': question, 'answer': answer, 'hint': hint}

def generate_copy_view_challenge():
    """Generate challenge for copy vs view"""
    array = np.random.randint(0, 10, size=random.randint(5, 10))
    operation = random.choice(['copy', 'view'])
    if operation == 'copy':
        question = f'Given the array a, write the code to create a deep copy (independent copy)'
        answer = 'np.copy(a)'
        hint = HINT_016
    else:
        question = f'Given the array a, write the code to create a view (shares memory)'
        answer = 'a.view()'
        hint = HINT_017
    return {'type': 'copy_view', 'question': question, 'answer': answer, 'hint': hint}

def generate_indexing_challenge():
    """Generate challenge for array indexing"""
    array = np.random.randint(0, 50, size=(random.randint(2, 4), random.randint(2, 4), random.randint(2, 3)))
    indices = tuple((random.randint(0, array.shape[i] - 1) for i in range(3)))
    question = f'Given the array a, write the code to access element at {indices}'
    answer = f'a[{indices[0]}, {indices[1]}, {indices[2]}]'
    hint = HINT_008
    return {'type': 'indexing', 'question': question, 'answer': answer, 'hint': hint}

def generate_join_challenge():
    """Generate challenge for joining arrays (stack, hstack, vstack)"""
    a = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
    b = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
    c = np.random.randint(0, 50, size=(random.randint(3, 5), random.randint(3, 5)))
    join_type = random.choice(['hstack', 'vstack', 'stack'])
    if join_type == 'hstack':
        question = f'Given the arrays a, b, and c, write the code to stack all three horizontally'
        answer = 'np.hstack([a, b, c])'
        hint = HINT_018
    elif join_type == 'vstack':
        question = f'Given the arrays a, b, and c, write the code to stack all three vertically'
        answer = 'np.vstack([a, b, c])'
        hint = HINT_019
    else:
        axis = random.choice([0, 1, 2])
        question = f'Given the arrays a, b, and c, write the code to stack them along axis {axis}'
        answer = f'np.stack([a, b, c], axis={axis})'
        hint = HINT_020
    return {'type': 'join', 'question': question, 'answer': answer, 'hint': hint}

def generate_split_challenge():
    """Generate challenge for splitting arrays"""
    array = np.random.randint(0, 50, size=(random.randint(4, 6), random.randint(4, 6)))
    axis = random.choice([0, 1])
    num_splits = random.choice([2, 3])
    question = f'Given the array a, write the code to split along axis {axis} into {num_splits} parts'
    answer = f'np.split(a, {num_splits}, axis={axis})'
    hint = HINT_009
    return {'type': 'split', 'question': question, 'answer': answer, 'hint': hint}

def generate_sort_challenge():
    """Generate challenge for sorting arrays"""
    array = np.random.randint(0, 50, size=random.randint(10, 20))
    kind = random.choice(['quicksort', 'mergesort', 'heapsort'])
    question = f'Given the array a, write the code to sort using {kind} algorithm'
    answer = f"np.sort(a, kind='{kind}')"
    hint = HINT_010
    return {'type': 'sort', 'question': question, 'answer': answer, 'hint': hint}

def generate_permutation_challenge():
    """Generate challenge for permutation and shuffling"""
    size = random.randint(10, 20)
    question = f'Write the code to create a random permutation of integers from 0 to {size - 1}'
    answer = f'np.random.permutation({size})'
    hint = HINT_011
    return {'type': 'permutation', 'question': question, 'answer': answer, 'hint': hint}

def generate_true_false_challenge(*, used_questions=None):
    """Generate true/false questions about array operations."""
    statements = [
        ('True or False: You can use -1 in reshape to automatically calculate one dimension.', 'True'),
        ('True or False: a.view() creates a new array object that shares the same data buffer.', 'True'),
        ('True or False: Multiple conditions can be combined with & (and) or | (or) for boolean indexing.', 'True'),
        ('True or False: a.sort() sorts the array in-place and returns None.', 'True'),
        ('True or False: np.concatenate() requires arrays to have the same shape along all axes except the concatenation axis.', 'True'),
        ('True or False: A 3D array with shape (2, 3, 4) has 24 elements total.', 'True'),
        ('True or False: a[::2] selects every other element starting from index 1.', 'False'),
        ('True or False: np.argmax(a) returns the maximum value.', 'False'),
        ('True or False: Fancy indexing (a[[0, 2, 4]]) always returns a view.', 'False'),
        ('True or False: np.arange(0, 10, 2) creates an array [0, 2, 4, 6, 8, 10].', 'False'),
    ]
    question, answer = pick_true_false_statement(statements, used_questions=used_questions)
    return {'type': 'true_false', 'question': question, 'answer': answer, 'hint': ''}

def play_game():
    """Run a single game session."""
    run_standard_game(
        teach_title='Array Blitz - Array Exercise',
        teach_body_lines=build_teach_body_lines(
            'You will get 20 single-line questions '
            '(15 code questions followed by 5 True/False questions).'
        ),
        validator_profile='default',
        code_generators=[
            generate_create_challenge,
            generate_shape_challenge,
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
            generate_permutation_challenge,
        ],
        true_false_factory=generate_true_false_challenge,
        background=EXERCISE_BACKGROUNDS["array_blitz"],
    )

def main():
    """Legacy entry — redirects learners to main.py (does not start a round)."""
    print('Use python3 main.py for the full menu.')
if __name__ == '__main__':
    main()
