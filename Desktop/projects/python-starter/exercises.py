"""
Python Practice Exercises
==========================

These exercises will help you practice:
- Basic syntax and statements
- Output (text and numbers)
- Comments
- Variables (including multiple and global variables)
- Data types (strings, integers, floats, booleans)
- Numbers and casting (int(), float(), str())

Complete each exercise by writing code below the comment.
You can test your solutions by running: python exercises.py
"""

# ============================================================================
# EASY QUESTIONS (5 questions)
# ============================================================================

# Exercise 1: Create a variable and print it
# Create a variable called "name" with the value "Alice"
# Then print the variable

name = "Alice"
print(name)


# Exercise 2: Multiple variables
# Create three variables:
#   - "first_name" with value "John"
#   - "last_name" with value "Doe"
#   - "age" with value 25
# Print each variable on a separate line

first_name = "John"
last_name = "Doe"
age = 25
print(first_name)
print(last_name)
print(age)


# Exercise 3: Different data types
# Create variables with different data types:
#   - "text" (string): "Python"
#   - "number" (integer): 100
#   - "decimal" (float): 3.14
#   - "is_true" (boolean): True
# Print each variable

text = "Python"
number = 100
decimal = 3.14
is_true = True
print(text)
print(number)
print(decimal)
print(is_true)

# Exercise 4: Basic arithmetic
# Create two variables: "a" = 10 and "b" = 5
# Print the result of a + b
# Print the result of a * b

a = 10
b = 5
print(a + b)
print(a * b)


# Exercise 5: Print text and numbers together
# Create a variable "score" = 95
# Print "Your score is" followed by the score value

score = 95
print("Your score is", score)


# ============================================================================
# MEDIUM QUESTIONS (13 questions)
# ============================================================================

# Exercise 6: Type casting - string to integer
# Create a variable "num_str" with the string value "50"
# Convert it to an integer using int() and store in "num_int"
# Print both the original string and the converted integer

num_str = "50"
num_int = int(num_str)
print(num_str)
print(num_int)

# Exercise 7: Type casting - integer to string
# Create a variable "age" with the integer value 30
# Convert it to a string using str() and store in "age_str"
# Print "I am" followed by the string version of age, followed by "years old"

age = 30
age_str = str(age)
print("I am", age_str, "years old")


# Exercise 8: Type casting - string to float
# Create a variable "price_str" with the string value "19.99"
# Convert it to a float using float() and store in "price_float"
# Print both values

price_str = 19.99
price_float = float(price_str)
print(price_str)
print(price_float)


# Exercise 9: Type casting - float to integer
# Create a variable "decimal_num" = 7.8 (float)
# Convert it to an integer using int() and store in "whole_num"
# Print both the float and the converted integer
# (Note: int() truncates, so 7.8 becomes 7)

decimal_num = 7.8
whole_num = int(decimal_num)
print(decimal_num)
print(whole_num)


# Exercise 10: Type casting - integer to float
# Create a variable "whole_num" = 42 (integer)
# Convert it to a float using float() and store in "decimal_num"
# Print both values

whole_num = 42
decimal_num = float(whole_num)
print(whole_num)
print(decimal_num)


# Exercise 11: Multiple variables with calculations
# Create three variables: "num1" = 15, "num2" = 3, "num3" = 7
# Calculate and print: num1 + num2 + num3
# Calculate and print: num1 * num2
# Calculate and print: num1 - num3

num1 = 15
num2 = 3
num3 = 7
print(num1 + num2 + num3)
print(num1 * num2)
print(num1 - num3)

# Exercise 12: Type casting in calculations
# Create a variable "num1_str" = "20" (string)
# Create a variable "num2" = 10 (integer)
# Convert num1_str to an integer, add it to num2, and print the result

num1_str = "20"
num2 = 10
result = int(num1_str) + num2
print(result)

# Exercise 13: String concatenation with casting
# Create variables: "item" = "book" (string), "quantity" = 3 (integer), "price" = 12.50 (float)
# Convert quantity to string and price to string
# Print: "I bought [quantity] [item]s for [price] dollars"
# Use string concatenation with the converted values

# YOUR CODE HERE


# Exercise 14: Mixing data types in output
# Create variables: "item" = "apple", "quantity" = 5, "price" = 2.50
# Print a sentence like: "I bought 5 apples for 2.5 dollars"
# Use all three variables in your print statement (Python will handle the conversion)

# YOUR CODE HERE


# Exercise 15: Multiple type conversions
# Create variables: "num_str1" = "15", "num_str2" = "25" (both strings)
# Convert both to integers, add them, and store in "sum_int"
# Convert sum_int to a string and print: "The sum is [sum]"

# YOUR CODE HERE


# Exercise 16: Calculations with mixed types
# Create variables: "base" = 100 (integer), "percentage_str" = "0.15" (string)
# Convert percentage_str to float
# Calculate: base * percentage (store in "result")
# Convert result to integer and print it

# YOUR CODE HERE


# Exercise 17: Global variable reassignment
# Create a global variable "counter" = 0 at the top level
# Print it
# Reassign it to 10 and print it
# Reassign it to 20 and print it

# YOUR CODE HERE


# Exercise 18: Complex string and number mixing
# Create variables: "product" = "shirt" (string), "price_str" = "29.99" (string), "quantity" = 2 (integer)
# Convert price_str to float
# Calculate total = price * quantity
# Print: "Product: [product]"
# Print: "Price per item: [price]"
# Print: "Quantity: [quantity]"
# Print: "Total: [total]"

# YOUR CODE HERE


# ============================================================================
# MORE INTENSE QUESTIONS (3 questions)
# ============================================================================

# Exercise 19: Complex variable operations
# Create the following variables:
#   - "base_price" = 100 (integer)
#   - "tax_rate_str" = "0.08" (string - represents 8% tax)
#   - "discount" = 15 (integer)
# 
# Convert tax_rate_str to a float
# Calculate: base_price * tax_rate (store in "tax_amount")
# Calculate: base_price + tax_amount - discount (store in "final_price")
# Print: "Base price:", base_price
# Print: "Tax:", tax_amount
# Print: "Discount:", discount
# Print: "Final price:", final_price

base_price = 100
tax_rate_str = "0.08"
discount = 15
tax_rate = float(tax_rate_str)
tax_amount = base_price * tax_rate
final_price = base_price + tax_amount - discount
print("Base price:", base_price)
print("Tax:", tax_amount)
print("Discount:", discount)
print("Final price:", final_price)

# Exercise 20: String and number formatting
# Create variables:
#   - "product" = "laptop" (string)
#   - "quantity_str" = "3" (string)
#   - "unit_price" = 999.99 (float)
# 
# Convert quantity_str to an integer
# Calculate total = quantity * unit_price
# Convert total to a string for display
# Print: "Product: laptop"
# Print: "Quantity: 3"
# Print: "Unit price: 999.99"
# Print: "Total: [calculated total]"

product = "laptop"


# Exercise 21: Multiple global variables and type conversions
# Create these global variables:
#   - "player_name" = "Alice" (string)
#   - "level_str" = "5" (string)
#   - "score" = 1250 (integer)
#   - "bonus_str" = "250.5" (string)
# 
# Convert level_str to integer, store in "level"
# Convert bonus_str to float, store in "bonus"
# Calculate total_score = score + bonus (convert bonus to int first)
# Print a formatted output showing:
#   Player name, level (as integer), score, bonus (as float), and total score
# Example format: "Player: Alice | Level: 5 | Score: 1250 | Bonus: 250.5 | Total: 1500"

# YOUR CODE HERE


# ============================================================================
# TESTING YOUR SOLUTIONS
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Running exercises...")
    print("=" * 60)
    print("\nIf you see this message, you need to complete the exercises above!")
    print("Add your code under each 'YOUR CODE HERE' comment.")
    print("\nTip: Work through exercises 1-5 first, then 6-18, then 19-21")
    print("Run this file to see your output!")
