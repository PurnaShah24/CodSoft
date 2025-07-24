# Simple Calculator

# Prompt the user for two numbers
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

# Ask the user to choose an operation
print("\nChoose an operation:")
print(" + for Addition")
print(" - for Subtraction")
print(" * for Multiplication")
print(" / for Division")

operation = input("Enter your choice of  Arithmatic operation (+, -, *, /): ")

if operation == '+':
    result = num1 + num2
    print(f"\nResult: {num1} + {num2} = {result}")
elif operation == '-':
    result = num1 - num2
    print(f"\nResult: {num1} - {num2} = {result}")
elif operation == '*':
    result = num1 * num2
    print(f"\nResult: {num1} * {num2} = {result}")
elif operation == '/':
    if num2 != 0:
        result = num1 / num2
        print(f"\nResult: {num1} / {num2} = {result}")
    else:
        print("\nError: Cannot divide by zero.")
else:
    print("\nInvalid operation. Please choose +, -, *, or /.")
