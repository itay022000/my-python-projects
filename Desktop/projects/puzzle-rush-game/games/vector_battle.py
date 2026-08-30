import numpy as np
import random
from exercise_session import run_standard_game
from session_common import EXERCISE_BACKGROUNDS, build_teach_body_lines, pick_true_false_statement
from hints import HINT_048, HINT_049, HINT_050, HINT_051, HINT_052, HINT_053, HINT_054, HINT_055, HINT_056, HINT_057, HINT_058, HINT_059, HINT_060
"""
Vector Battle - Master NumPy random operations and permutations

This game challenges you to:
- Understand np.random.permutation() vs np.random.shuffle()
- Work with random number generation
- Understand data distributions
- Use np.random.choice() and np.random.randint()
"""


def generate_permutation_challenge():
    """Generate challenge for np.random.permutation()"""
    question_type = random.choice(['create', 'range', 'property'])
    question_type = random.choice(['create', 'range', 'property', '2d', 'copy', 'scenario'])
    if question_type == 'create':
        array = np.random.randint(0, 20, size=random.randint(8, 15))
        question = f'Given the array a, write the code to generate a permuted copy (original stays unchanged)'
        answer = 'np.random.permutation(a)'
    elif question_type == 'range':
        size = random.randint(10, 20)
        question = f'Write the code to randomly order the sequence [0, 1, 2, ..., {size - 1}]'
        answer = f'np.random.permutation({size})'
    elif question_type == 'property':
        question = "What is the return value type of np.random.permutation(a)?\nWrite 'array' or 'none'"
        answer = 'array'
    elif question_type == '2d':
        array = np.random.randint(0, 30, size=(random.randint(3, 5), random.randint(3, 5)))
        question = f'Given the array a, write the code to permute the rows (returns new array)'
        answer = 'np.random.permutation(a)'
    elif question_type == 'copy':
        array = np.random.randint(0, 25, size=random.randint(10, 15))
        question = f'Given the array a, you need a shuffled version but must preserve the original. Write the code'
        answer = 'np.random.permutation(a)'
    else:
        question = 'You have an array and need to create multiple independent shuffled versions. Which function should you use?\nWrite permutation/shuffle only'
        answer = 'permutation'
    hint = HINT_048
    return {'type': 'permutation', 'question': question, 'answer': answer, 'hint': hint}

def generate_shuffle_challenge():
    """Generate challenge for np.random.shuffle()"""
    question_type = random.choice(['inplace', 'property', 'modify'])
    question_type = random.choice(['inplace', 'property', 'modify', '2d', 'memory', 'scenario'])
    if question_type == 'inplace':
        array = np.random.randint(0, 50, size=(random.randint(3, 6), random.randint(3, 6)))
        question = f'Given the array a, write the code to shuffle rows (modifies original)'
        answer = 'np.random.shuffle(a)'
    elif question_type == 'property':
        question = 'Which function modifies arrays in-place and returns None?\nWrite permutation/shuffle only'
        answer = 'shuffle'
    elif question_type == 'modify':
        array = np.random.randint(0, 30, size=random.randint(10, 15))
        question = f'Given the array a, write the code to randomly reorder elements (destructive operation)'
        answer = 'np.random.shuffle(a)'
    elif question_type == '2d':
        array = np.random.randint(0, 40, size=(random.randint(4, 6), random.randint(4, 6)))
        question = f'Given the array a, write the code to randomly rearrange rows in-place (no copy created)'
        answer = 'np.random.shuffle(a)'
    elif question_type == 'memory':
        question = 'Given the array a, you want to shuffle it without creating a copy to save memory. Write the code'
        answer = 'np.random.shuffle(a)'
    else:
        question = "You need to shuffle an array and don't need the original order. Which function is more memory-efficient?\nWrite permutation/shuffle only"
        answer = 'shuffle'
    hint = HINT_049
    return {'type': 'shuffle', 'question': question, 'answer': answer, 'hint': hint}

def generate_distribution_challenge():
    """Generate challenge for random number generation"""
    question_type = random.choice(['single', 'multiple', 'range', 'negative'])
    question_type = random.choice(['single', 'multiple', 'range', 'negative', '3d', 'large', 'edge'])
    if question_type == 'single':
        low = random.randint(-20, 0)
        high = random.randint(1, 50)
        question = f'Write the code to generate a random integer between {low} and {high - 1}'
        answer = f'np.random.randint({low}, {high})'
    elif question_type == 'multiple':
        low = random.randint(-20, 0)
        high = random.randint(1, 50)
        shape = (random.randint(3, 5), random.randint(3, 5))
        question = f'Write the code to generate a 2D array with shape {shape} of random integers from {low} to {high - 1}'
        answer = f'np.random.randint({low}, {high}, size={shape})'
    elif question_type == 'range':
        high = random.randint(20, 40)
        shape = (random.randint(3, 5), random.randint(3, 5))
        question = f'Write the code to generate a 2D array with shape {shape} of random integers from 0 to {high - 1}'
        answer = f'np.random.randint({high}, size={shape})'
    elif question_type == 'negative':
        low = random.randint(-30, -10)
        high = random.randint(10, 40)
        shape = (random.randint(4, 6), random.randint(4, 6))
        question = f'Write the code to generate a 2D array with shape {shape} of random integers between {low} and {high - 1}'
        answer = f'np.random.randint({low}, {high}, size={shape})'
    elif question_type == '3d':
        low = random.randint(-10, 0)
        high = random.randint(1, 30)
        shape = (random.randint(2, 3), random.randint(2, 3), random.randint(2, 3))
        question = f'Write the code to generate a 3D array with shape {shape} of random integers from {low} to {high - 1}'
        answer = f'np.random.randint({low}, {high}, size={shape})'
    elif question_type == 'large':
        low = random.randint(-50, -20)
        high = random.randint(20, 100)
        size = random.randint(15, 25)
        question = f'Write the code to generate {size} random integers between {low} and {high - 1}'
        answer = f'np.random.randint({low}, {high}, size={size})'
    else:
        question = 'Write the code to generate a random integer from 0 to 99 (inclusive)'
        answer = 'np.random.randint(100)'
    hint = HINT_050
    return {'type': 'distribution', 'question': question, 'answer': answer, 'hint': hint}

def generate_choice_challenge():
    """Generate challenge for np.random.choice()"""
    question_type = random.choice(['single', 'multiple', 'replace', 'weights'])
    question_type = random.choice(['single', 'multiple', 'replace', 'weights', 'large', 'unique', 'scenario'])
    if question_type == 'single':
        array = np.random.randint(0, 50, size=random.randint(8, 15))
        question = f'Given the array a, write the code to randomly choose one element'
        answer = 'np.random.choice(a)'
    elif question_type == 'multiple':
        array = np.random.randint(0, 50, size=random.randint(8, 15))
        size = random.randint(3, 6)
        question = f'Given the array a, write the code to randomly select {size} elements (with replacement)'
        answer = f'np.random.choice(a, size={size}, replace=True)'
    elif question_type == 'replace':
        array = np.random.randint(0, 50, size=random.randint(8, 15))
        size = random.randint(3, 6)
        replace = random.choice([True, False])
        question = f'Given the array a, write the code to randomly select {size} elements (replace={replace})'
        answer = f'np.random.choice(a, size={size}, replace={replace})'
    elif question_type == 'weights':
        array = np.random.randint(0, 50, size=random.randint(8, 12))
        size = random.randint(3, 5)
        question = f'Given the array a, write the code to randomly pick {size} elements without replacement'
        answer = f'np.random.choice(a, size={size}, replace=False)'
    elif question_type == 'large':
        array = np.random.randint(0, 100, size=random.randint(15, 25))
        size = random.randint(5, 10)
        question = f'Given the array a, write the code to randomly select {size} elements (with replacement)'
        answer = f'np.random.choice(a, size={size}, replace=True)'
    elif question_type == 'unique':
        array = np.random.randint(0, 50, size=random.randint(10, 15))
        size = random.randint(4, 7)
        question = f'Given the array a, write the code to randomly pick {size} unique elements (no duplicates)'
        answer = f'np.random.choice(a, size={size}, replace=False)'
    else:
        array_size = random.randint(8, 12)
        array = np.random.randint(0, 30, size=array_size)
        sample_size = array_size + 3
        question = f'Given the array a, you need to sample more elements than the array size. Write the code to select {sample_size} elements'
        answer = f'np.random.choice(a, size={sample_size}, replace=True)'
    hint = HINT_051
    return {'type': 'choice', 'question': question, 'answer': answer, 'hint': hint}

def generate_comparison_challenge():
    """Generate challenge comparing shuffle vs permutation"""
    question_type = random.choice(['difference', 'use_case', 'return', 'property'])
    question_type = random.choice(['difference', 'use_case', 'return', 'property', 'memory', 'chain', 'error'])
    _shuffle_copy_hint = HINT_052
    _returns_value_hint = HINT_053
    if question_type == 'difference':
        if random.choice([True, False]):
            question = 'Given the array a, write the code to shuffle it in-place (modifies original, returns None)'
            answer = 'np.random.shuffle(a)'
        else:
            question = 'Given the array a, write the code to create a shuffled copy without modifying the original'
            answer = 'np.random.permutation(a)'
        hint = _shuffle_copy_hint
    elif question_type == 'use_case':
        scenario = random.choice(['preserve', 'memory', 'multiple'])
        if scenario == 'preserve':
            array = np.random.randint(0, 20, size=random.randint(8, 12))
            question = f'Given the array a, you need both the original and shuffled version. Write the code to get shuffled copy'
            answer = 'np.random.permutation(a)'
        elif scenario == 'memory':
            question = 'Given the array a, you have limited memory and want to shuffle it. Write the code (use in-place operation)'
            answer = 'np.random.shuffle(a)'
        else:
            question = 'Given the array a, you need 3 different shuffled versions of it. Write the code for one shuffle (use function that returns new array)'
            answer = 'np.random.permutation(a)'
        hint = HINT_055
    elif question_type == 'return':
        if random.choice([True, False]):
            question = "What does np.random.shuffle(a) return?\nWrite 'none' or 'array'"
            answer = 'none'
        else:
            question = "What does np.random.permutation(a) return?\nWrite 'none' or 'array'"
            answer = 'array'
        hint = _returns_value_hint
    elif question_type == 'property':
        question = 'Given the array a, write the code to randomly rearrange it and get a new array back'
        answer = 'np.random.permutation(a)'
        hint = HINT_058
    elif question_type == 'memory':
        question = 'Which function is better for memory-constrained environments when shuffling large arrays?\nWrite permutation/shuffle only'
        answer = 'shuffle'
        hint = HINT_059
    elif question_type == 'chain':
        question = 'You want to chain operations: shuffled = shuffle(a) and then use shuffled. Which function allows this?\nWrite permutation/shuffle only'
        answer = 'permutation'
        hint = _returns_value_hint
    else:
        question = "If you try to assign result = np.random.shuffle(a), what will result be?\nWrite 'none' or 'array'"
        answer = 'none'
        hint = HINT_060
    return {'type': 'comparison', 'question': question, 'answer': answer, 'hint': hint}

def generate_random_array_challenge():
    """Generate challenge for creating random arrays"""
    question_type = random.choice(['random', 'uniform', 'seed'])
    if question_type == 'random':
        shape = (random.randint(3, 5), random.randint(3, 5), random.randint(2, 3))
        question = f'Write the code to generate a 3D array with shape {shape} of random floats between 0 and 1'
        answer = f'np.random.random({shape})'
        hint = HINT_054
    elif question_type == 'uniform':
        low = random.randint(1, 10)
        high = random.randint(11, 30)
        shape = (random.randint(3, 5), random.randint(3, 5))
        question = f'Write the code to generate a 2D array with shape {shape} of random floats between {low} and {high}\nInclude the bounds stated above in your solution.'
        answer = f'np.random.uniform({low}, {high}, size={shape})'
        hint = HINT_056
    else:
        seed = random.randint(0, 1000)
        question = f'Write the code to initialize the random number generator with seed {seed}'
        answer = f'np.random.seed({seed})'
        hint = HINT_057
    return {'type': 'random_array', 'question': question, 'answer': answer, 'hint': hint}

def generate_true_false_challenge(*, used_questions=None):
    """Generate true/false questions about random operations."""
    statements = [
        ('True or False: np.random.choice(a, size=5, replace=False) requires the array to have at least 5 elements.', 'True'),
        ('True or False: np.random.randint(-10, 10) can generate negative integers.', 'True'),
        ('True or False: np.random.random() generates values in the range [0, 1) (0 inclusive, 1 exclusive).', 'True'),
        ('True or False: For memory efficiency with large arrays, shuffle() is better than permutation().', 'True'),
        ('True or False: permutation() always returns a copy, never a view.', 'True'),
        ('True or False: shuffle() is an in-place operation that modifies the original array.', 'True'),
        ('True or False: np.random.permutation() only works with 1D arrays.', 'False'),
        ('True or False: np.random.shuffle() shuffles all axes independently for 2D arrays.', 'False'),
        ('True or False: Setting a seed only affects the next random operation, not subsequent ones.', 'False'),
        ('True or False: np.random.uniform(1, 10, size=5) generates 5 floats in the closed interval [1, 10] (both endpoints included).', 'False'),
    ]
    question, answer = pick_true_false_statement(statements, used_questions=used_questions)
    return {'type': 'true_false', 'question': question, 'answer': answer, 'hint': ''}

def play_game():
    """Run a single game session."""
    run_standard_game(teach_title='Vector Battle - Vector Exercise', teach_body_lines=build_teach_body_lines('You will get 20 single-line questions (15 code questions followed by 5 True/False questions).'), validator_profile='vector', code_generators=[generate_permutation_challenge, generate_shuffle_challenge, generate_distribution_challenge, generate_choice_challenge, generate_comparison_challenge, generate_random_array_challenge], true_false_factory=generate_true_false_challenge, background=EXERCISE_BACKGROUNDS["vector_battle"])

def main():
    """Legacy entry — redirects learners to main.py (does not start a round)."""
    print('Use python3 main.py for the full menu.')
if __name__ == '__main__':
    main()
