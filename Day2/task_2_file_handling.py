import json
import math 


# loading json data  function
def load_employees() -> list[dict]:
    """Load employee data from JSON file."""

    try:
        with open("employees.json", "r", encoding="utf-8") as file:
            employees = json.load(file)
            return employees

    except FileNotFoundError:
        print("Employee file not found. Creating an empty list.")
        return []

    except json.JSONDecodeError:
        raise ValueError("Employee JSON file contains invalid data.")

    if not isinstance(employees, list):
        raise ValueError("Employee JSON must contain a list.")

    for employee in employees:
        if not isinstance(employee, dict):
            raise ValueError("Each employee must be a dictionary.")
        
    return employee
    



# save_employees function
def save_employees(employees: list[dict]) -> None:
    """Save employee data into JSON file."""

    with open("employees.json", "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)

    print("Employee data saved successfully!")



import math


def validate_employee_id(employee_id: int) -> None:
    """Validate employee ID."""

    if isinstance(employee_id, bool) or not isinstance(employee_id, int):
        raise ValueError("Employee ID must be an integer.")

    if employee_id <= 0:
        raise ValueError("Employee ID must be positive.")


def validate_salary(salary: float) -> None:
    """Validate employee salary."""

    if isinstance(salary, bool) or not isinstance(salary, (int, float)):
        raise ValueError("Salary must be numeric.")

    if not math.isfinite(salary):
        raise ValueError("Salary must be a finite number.")

    if salary < 0:
        raise ValueError("Salary cannot be negative.")


def validate_text(value: str, field_name: str) -> str:
    """Validate and normalize text input."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")

    return value.strip()



def validate_email(email: str) -> str:
    """Validate basic email format."""

    email = validate_text(email, "Email")

    if email.count("@") != 1:
        raise ValueError("Invalid email format.")

    local, domain = email.split("@")

    if not local or "." not in domain:
        raise ValueError("Invalid email format.")

    if domain.startswith(".") or domain.endswith("."):
        raise ValueError("Invalid email format.")

    return email
    


# step 1: add_employee function
def add_employee(id: int, name: str, email: str, department: str, salary: float) -> list[dict]:
    """
    Add a new employee and save employee details to JSON file.

    Args:
        id (int): Unique employee ID.
        name (str): Employee name.
        email (str): Employee email address.
        department (str): Employee department.
        salary (float): Employee salary.

    Returns:
        list[dict]: Updated list of employees.

    Raises:
        ValueError: If employee details are invalid or ID already exists.
 """
    
    # Check empty values
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")

    if not email or not email.strip():
        raise ValueError("Email cannot be empty")
        

    if not department or not department.strip():
        raise ValueError("Department cannot be empty")
        

    if salary is None:
        raise ValueError("Salary cannot be empty")
        
    validate_employee_id(id)
    validate_salary(salary)
    name = validate_text(name, "Name")
    email = validate_email(email)
    department = validate_text(department, "Department")


    employees = load_employees()
    
    # Check for duplicate employee ID
    for employee in employees:
        if employee["id"] == id:
            raise ValueError("Employee ID already exists.")
        
    employee = {
        "id": id,
        "name": name,
        "email": email,
        "department": department,
        "salary": salary
    }
    employees.append(employee)

    save_employees(employees)

    print("Employee added successfully!")
    return employees




# step 2: Display all employee details from the JSON file
def display_employees():

    # load data 
    employees =load_employees()
    if not employees:
        print("No employees found.")
        return
    for employee in employees:
        print(f"ID: {employee['id']}, Name: {employee['name']}, Email: {employee['email']}, Department: {employee['department']}, Salary: {employee['salary']}")



# step 3:Search for an employee by ID

def search_employee_by_id(employee_id: int):
    employees = load_employees()
    if not employees:
        print("No employees found.")
        return
    for employee in employees:
        if employee['id'] == employee_id:
            print(f"ID: {employee['id']}, Name: {employee['name']}, Email: {employee['email']}, Department: {employee['department']}, Salary: {employee['salary']}")
            return  
    print("Employee not found.")



# step 3: Update an employee department or salary.


def update_employee(employee_id: int, department: str = None, salary: float = None)-> None:
    """Update an employee's department or salary based on their ID."""
    
    employees = load_employees()
    if not employees:
            print("No employees found.")
            return
    for employee in employees:
        if employee['id'] == employee_id:
            if department is not None:
                employee['department'] = department
            if salary is not None:
                employee['salary'] = salary

            save_employees(employees)
            print("Employee updated successfully!")
            return
    print("Employee not found.")





# step 4: Delete an employee by ID


def delete_employee(employee_id: int) -> None:
    """Delete an employee based on their ID."""

    employees = load_employees()
    if not employees:
        print("No employees found.")
        return
    for i, employee in enumerate(employees):
        if employee['id'] == employee_id:
            del employees[i]
            save_employees(employees)
            print("Employee deleted successfully!")
            return
    print("Employee not found.")



# step 5: Display the total number of employees.

def total_employees() -> int:
    """Return the total number of employees."""

    employees = load_employees()
    
    count = len(employees)
    print(f"Total employees: {count}")
    return count





def main():

    while True:

        print("\n===== Employee Management System =====")
        print("1. Add Employee")
        print("2. Display All Employees")
        print("3. Search Employee by ID")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Total Employees")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:

            if choice == "1":
                employee_id = int(input("Enter Employee ID: "))
                name = input("Enter Name: ")
                email = input("Enter Email: ")
                department = input("Enter Department: ")
                salary = float(input("Enter Salary: "))

                add_employee(employee_id, name, email, department, salary)

            elif choice == "2":
                display_employees()

            elif choice == "3":
                employee_id = int(input("Enter Employee ID: "))
                search_employee_by_id(employee_id)

            elif choice == "4":
                employee_id = int(input("Enter Employee ID: "))

                department = input(
                    "Enter new Department (press Enter to skip): "
                )

                salary_input = input(
                    "Enter new Salary (press Enter to skip): "
                )

                department = department if department else None
                salary = float(salary_input) if salary_input else None

                update_employee(employee_id, department, salary)

            elif choice == "5":
                employee_id = int(input("Enter Employee ID: "))
                delete_employee(employee_id)

            elif choice == "6":
                total_employees()

            elif choice == "7":
                print("Thank you for using Employee Management System!")
                break

            else:
                print("Invalid choice! Please select between 1 and 7.")

        except ValueError as error:
            print(f"Error: {error}")


# Program execution
if __name__ == "__main__":
    main()
