# # 1 • Take name, age, email and city from the user and display a formatted introduction.
def Intro():
    name = input("Enter your name: ").strip()
    age = input("Enter your age: ").strip()
    email = input("Enter your email: ").strip()
    city = input("Enter your city: ").strip()
    
    # required all fields
    if not name or not age or not email or not city:
        print("All fields are required. Please provide valid inputs.")
        return 
    
    # validate age input
    try:
        age = int(age)
        if age <= 0 or age > 100:
           print("Age must be between 1 and 100.")
           return None
    except ValueError:
        print("Please enter a valid numeric age.")
        return None


    # email validation
    if "@" not in email or "." not in email:
        print("Please enter a valid email address.")
        return None
    
    
    introduction = f"Hello, my name is {name}. I am {age} years old, and I live in {city}. You can reach me at {email}."
    return introduction
    
introduction =  Intro()
print(introduction)



# # 2 • Build a calculator for addition, subtraction, multiplication, division and modulus.

def calculator():
    print("===== Simple Calculator =====")
    print("Operations: +, -, *, /, %")

    try:
        num1 = input("Enter first number: ").strip()
        num2 = input("Enter second number: ").strip()
        operator = input("Enter operator: ").strip()

        # Handle empty input
        if not num1 or not num2:
            print("Error: Number input cannot be empty.")
            return

        # Validate numeric input
        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:
            print("Error: Please enter valid numeric values.")
            return

        # Perform calculation
        if operator == "+":
            result = num1 + num2

        elif operator == "-":
            result = num1 - num2

        elif operator == "*":
            result = num1 * num2

        elif operator == "/":
            if num2 == 0:
                print("Error: Division by zero is not allowed.")
                return
            result = num1 / num2

        elif operator == "%":
            if num2 == 0:
                print("Error: Modulus by zero is not allowed.")
                return
            result = num1 % num2

        else:
            print("Error: Invalid operator.")
            return

        print(f"Result: {result}")

    except Exception as e:
        print(f"Unexpected error: {e}")


cal = calculator()





#  Convert Celsius to Fahrenheit.
def celsius_to_fahrenheit(celsius):
    try:
        fahrenheit = (celsius * 9/5) + 32
        return fahrenheit
    except TypeError:
        print("Error: Please provide a numeric value for Celsius.")
        return None
    
input_celsius = input("Enter temperature in Celsius: ").strip()

if not input_celsius:
    print("Error: Celsius input cannot be empty.")
elif not input_celsius.replace('.', '').isdigit():
    print("Error: Please enter a valid numeric value for Celsius.")
else:
    fahrenheit = celsius_to_fahrenheit(float(input_celsius))
    print(f"Fahrenheit: {fahrenheit}")




# # Calculate rectangle area and perimeter

def rectangle():
    try:
        length = input("Enter length: ").strip()
        width = input("Enter width: ").strip()

        # Handle empty input
        if not length or not width:
            print("Error: Length and width cannot be empty.")
            return

        # Validate numeric input
        length = float(length)
        width = float(width)

        # Validate positive values
        if length <= 0 or width <= 0:
            print("Error: Length and width must be positive.")
            return

        # Calculate area and perimeter
        area = length * width
        perimeter = 2 * (length + width)

        print(f"Area: {area}")
        print(f"Perimeter: {perimeter}")

    except ValueError:
        print("Error: Please enter valid numeric values.")


rectangle()



# Calculate a salary after an 18 percent increment

def calculate_salary_increment(salary):
    try:
        incremented_salary = salary * 1.18
        return incremented_salary
    except TypeError:
        print("Error: Please provide a numeric value for salary.")
        return None

salary_input = input("Enter current salary: ").strip()
if not salary_input:
    print("Error: Salary input cannot be empty.")
elif not salary_input.replace('.', '').isdigit():
    print("Error: Please enter a valid numeric value for salary.")
else:
    new_salary = calculate_salary_increment(float(salary_input))
    print(f"Salary after 18% increment: {new_salary}")
    
 