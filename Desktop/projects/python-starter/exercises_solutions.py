"""
SOLUTIONS to Python Practice Exercises
======================================

⚠️  Try to solve the exercises yourself first!
Only look at these solutions if you're really stuck.

These solutions show one way to solve each problem.
There are often multiple correct approaches!
"""

# ============================================================================
# EASY QUESTIONS - SOLUTIONS
# ============================================================================

# Exercise 1: Create a variable and print it
name = "Alice"
print(name)

# Exercise 2: Multiple variables
first_name = "John"
last_name = "Doe"
age = 25
print(first_name)
print(last_name)
print(age)

# Exercise 3: Different data types
text = "Python"
number = 100
decimal = 3.14
is_true = True
print(text)
print(number)
print(decimal)
print(is_true)

# Exercise 4: Basic arithmetic
a = 10
b = 5
print(a + b)
print(a * b)

# Exercise 5: Print text and numbers together
score = 95
print("Your score is", score)
# Alternative: print("Your score is " + str(score))

# ============================================================================
# MEDIUM QUESTIONS - SOLUTIONS
# ============================================================================

# Exercise 6: Type casting - string to integer
num_str = "50"
num_int = int(num_str)
print(num_str)
print(num_int)

# Exercise 7: Type casting - integer to string
age = 30
age_str = str(age)
print("I am", age_str, "years old")
# Alternative: print("I am " + age_str + " years old")

# Exercise 8: Type casting - string to float
price_str = "19.99"
price_float = float(price_str)
print(price_str)
print(price_float)

# Exercise 9: Type casting - float to integer
decimal_num = 7.8
whole_num = int(decimal_num)
print(decimal_num)
print(whole_num)

# Exercise 10: Type casting - integer to float
whole_num = 42
decimal_num = float(whole_num)
print(whole_num)
print(decimal_num)

# Exercise 11: Multiple variables with calculations
num1 = 15
num2 = 3
num3 = 7
print(num1 + num2 + num3)
print(num1 * num2)
print(num1 - num3)

# Exercise 12: Type casting in calculations
num1_str = "20"
num2 = 10
result = int(num1_str) + num2
print(result)

# Exercise 13: String concatenation with casting
item = "book"
quantity = 3
price = 12.50
quantity_str = str(quantity)
price_str = str(price)
print("I bought " + quantity_str + " " + item + "s for " + price_str + " dollars")
# Alternative: print("I bought", quantity, item + "s", "for", price, "dollars")

# Exercise 14: Mixing data types in output
item = "apple"
quantity = 5
price = 2.50
print("I bought", quantity, item + "s", "for", price, "dollars")

# Exercise 15: Multiple type conversions
num_str1 = "15"
num_str2 = "25"
sum_int = int(num_str1) + int(num_str2)
sum_str = str(sum_int)
print("The sum is " + sum_str)
# Alternative: print("The sum is", sum_int)

# Exercise 16: Calculations with mixed types
base = 100
percentage_str = "0.15"
percentage = float(percentage_str)
result = base * percentage
result_int = int(result)
print(result_int)

# Exercise 17: Global variable reassignment
counter = 0
print(counter)
counter = 10
print(counter)
counter = 20
print(counter)

# Exercise 18: Complex string and number mixing
product = "shirt"
price_str = "29.99"
quantity = 2
price = float(price_str)
total = price * quantity
print("Product:", product)
print("Price per item:", price)
print("Quantity:", quantity)
print("Total:", total)

# ============================================================================
# MORE INTENSE QUESTIONS - SOLUTIONS
# ============================================================================

# Exercise 19: Complex variable operations
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
product = "laptop"
quantity_str = "3"
unit_price = 999.99

quantity = int(quantity_str)
total = quantity * unit_price
total_str = str(total)

print("Product:", product)
print("Quantity:", quantity)
print("Unit price:", unit_price)
print("Total:", total_str)
# Or: print("Total:", total)  # Python will convert automatically

# Exercise 21: Multiple global variables and type conversions
player_name = "Alice"
level_str = "5"
score = 1250
bonus_str = "250.5"

level = int(level_str)
bonus = float(bonus_str)
total_score = score + int(bonus)

print("Player:", player_name, "| Level:", level, "| Score:", score, "| Bonus:", bonus, "| Total:", total_score)
# Alternative formatting:
# print("Player: " + player_name + " | Level: " + str(level) + " | Score: " + str(score) + " | Bonus: " + str(bonus) + " | Total: " + str(total_score))
