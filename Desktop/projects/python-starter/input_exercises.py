"""
User Input Practice Exercises
===============================

These exercises will help you practice:
- The input() function
- Getting user input
- Converting input to different types
- Using input in your programs

Complete each exercise by writing code below the comment.
You can test your solutions by running: python input_exercises.py
"""

# ============================================================================
# USER INPUT EXERCISES (5 exercises)
# ============================================================================

# Exercise 1: Basic input
# Ask the user for their name using input()
# Store it in a variable called "name"
# Print a greeting using f-strings: "Hello, [name]!"

name = input("Enter your name: ")
print(f"Hello, {name}!")


# Exercise 2: Input with type conversion
# Ask the user for their age using input()
# Convert the input to an integer
# Store it in a variable called "age"
# Print: "You are [age] years old"

ageStr = input("Enter your age: ")
age = int(ageStr)
print(f"You are {age} years old")


# Exercise 3: Input in conditional
# Ask the user: "What is 2 + 2?"
# Store their answer
# If their answer equals "4" (as a string), print "Correct!"
# Otherwise, print "Wrong!"

result = input("What is 2 + 2?")
if result == "4":
    print("Correct!")
else:
    print("Wrong!")

# Exercise 4: Multiple inputs
# Ask the user for three things:
#   1. Their favorite color
#   2. Their favorite food
#   3. Their favorite number (as a string, then convert to integer)
# Store each in a variable
# Print all three using f-strings in one sentence

color = input("Enter your favorite color: ")
food = input("Enter your favorite food: ")
numberStr = input("Enter your favorite number: ")
number = int(numberStr)
print(f"Your favorite color is {color}, your favorite food is {food}, and your favorite number is {number}")


# Exercise 5: Input with calculation
# Ask the user for a number (as input, then convert to float)
# Ask the user for another number (as input, then convert to float)
# Calculate the sum of the two numbers
# Print: "The sum of [first] and [second] is [sum]"

numberStr1 = input("Enter your first number: ")
number1 = float(numberStr1)
numberStr2 = input("Enter your second number: ")
number2 = float(numberStr2)
sum = number1 + number2
print(f"The sum of {number1} and {number2} is {sum}")

# ============================================================================
# TESTING YOUR SOLUTIONS
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("User Input Exercises")
    print("=" * 60)
    print("\nRun this file and test your exercises!")
    print("Make sure to test with different inputs to verify your code works correctly.")

