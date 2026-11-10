# Print even numbers from 1 to 100.

def even_no(nums):
  even_list = []
  for num in range(1,nums+1): 
    if num % 2 == 0:
      even_list.append(num)
  return even_list

nums = 100
even = even_no(nums)
print(f"Even no : {even}")







# Check positive, negative or zero


def check_no(num):

    # Handle empty input
    if not num.strip():
        return "Error: Input cannot be empty."

    # Validate numeric input
    try:
        num = float(num)

    except ValueError:
        return "Error: Please enter a valid number."

    # Check positive, negative or zero
    if num > 0:
        return "This is a positive number."

    elif num < 0:
        return "This is a negative number."

    else:
        return "The number is zero."


num = input("Enter your number: ")

  
result = check_no(num)
print(result)







# • Check even or odd.

def check_even_or_odd(num):

    # Handle empty input
    if not num.strip():
        return "Error: Input cannot be empty."
    # Validate numeric input
    try:
        num = float(num)
    except ValueError:
        return "Error: Please enter a valid number."

    if num % 2==0:
      return "EVEN"
    else:
      return "ODD"
      
 
num = input("Enter your number: ")
result = check_even_or_odd(num)
print(result)






# Find the largest of three numbers.


def find_largest(num1, num2, num3):

    # Handle empty input
    if not num1.strip() or not num2.strip() or not num3.strip():
        return "Error: All three inputs are required."

    # Validate numeric input
    try:
        num1 = float(num1)
        num2 = float(num2)
        num3 = float(num3)

    except ValueError:
        return "Error: Please enter valid numbers."

    # Find the largest number
    if num1 >= num2 and num1 >= num3:
        return f"Largest number is: {num1}"

    elif num2 >= num1 and num2 >= num3:
        return f"Largest number is: {num2}"

    else:
        return f"Largest number is: {num3}"


 
num1 = input("Enter first number: ")
num2 = input("Enter second number: ")
num3 = input("Enter third number: ")

  
result = find_largest(num1, num2, num3)

print(result)





# Print a multiplication table

def multiplication_table(num):

    # Handle empty input
    if not num.strip():
        return "Error: Input cannot be empty."

    # Validate numeric input
    try:
        num = int(num)
    except ValueError:
        return "Error: Please enter a valid integer."

    # Print multiplication table
    for i in range(1, 11):
        print(f"{num} x {i} = {num * i}")

 
num = input("Enter a number: ")
result = multiplication_table(num)
print(result)


#  Calculate the sum from 1 to n.
def calculate_sum(n):
    # Handle empty input
    if not n.strip():
        return "Error: Input cannot be empty."

    # Validate numeric input
    try:
        n = int(n)
    except ValueError:
        return "Error: Please enter a valid integer."

    # Calculate the sum from 1 to n
    total_sum = sum(range(1, n + 1))

    return total_sum

n = input("Enter a number: ")
result = calculate_sum(n)
print(result)


# • Check whether a number is prime

def is_prime_no(num):

    # Handle empty input
    if not num.strip():
        return "Error: Input cannot be empty."

    # Validate numeric input
    try:
        num = int(num)
    except ValueError:
        return "Error: Please enter a valid integer."

    # Check prime condition
    if num <= 1:
        return "Not a prime number."
    is_prime = True
    for i in range(2, num):
        if num % i == 0:
            is_prime = False 
            break
    return is_prime


num = input("Enter your number: ")

# Call function
result = is_prime_no(num)
print(result)


