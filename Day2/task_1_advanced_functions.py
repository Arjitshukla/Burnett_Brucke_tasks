from typing import Any, Callable
from time import perf_counter
from functools import wraps

# step 1: Salary Validation Function [resuable function]


def validate_salaries(salaries: tuple[float, ...]) -> None:
    """Validate salary input."""

    if not salaries:
        raise ValueError("At least one salary is required.")

    for salary in salaries:

        if isinstance(salary, bool) or not isinstance(salary, (int, float)):
            raise TypeError("Salary must be numeric.")

        if salary <= 0:
            raise ValueError("Salary must be greater than zero.")


def execution_logger(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to log the function name and execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = perf_counter()

        print("Execution started..")
        print(f"Function name: {func.__name__}")
        try:
            result = func(*args, **kwargs)

            print("Execution completed.")

            return result

        finally:
            end = perf_counter()
            print(f"Execution time: {end - start:.6f} seconds")

    return wrapper



@execution_logger
def employee_details(**detail:dict):
    """Accept employee details using keyword arguments."""
    if not detail:
       raise ValueError("Employee details cannot be empty.")
    print("Employee detail")
    for key,value in detail.items():
      print(f"{key}:{value}")
    
employee_details(name="Arjit", age=24, department="SDE", position="Manager")



# step 2: Function to calculate salary statistics

@execution_logger
def employee_salary(*salary:float)-> tuple[float, float, float, float]:
  """calculate salary statistics like total, average, highest and lowest salary"""
  # validation over salary
  validate_salaries(salary)  # resuable function to validate salary
  total = sum(salary)
  average = total/len(salary)
  highest = max(salary)
  lowest = min(salary)
  return total,average,highest,lowest

result = employee_salary(10000, 20000, 30000)
print(f"total salary : {result[0]}")
print(f"average salary : {result[1]}")
print(f"highest salary : {result[2]}")
print(f"lowest salary : {result[3]}")   
  

  
# step 3: Closure for running total

def running_total():
    """Create a closure that maintains a running total."""

    total = 0

    def add_amount(amount: float) -> float:
        nonlocal total

        validate_salaries((amount,))
        total += amount

        return total

    return add_amount
new_ammount = running_total()
print(new_ammount(1000))  # Output: 1000 
print(new_ammount(2000))  # Output: 3000


    
