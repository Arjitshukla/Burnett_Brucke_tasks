employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya", "department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary": 55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department": "Development", "salary": 60000}
]


#  first : Use list comprehension to get all employee names.

all_employee_name  = [emp['name']  for emp in employees]
print(all_employee_name)


# second : Get employees earning more than 45,000
employees_name = [emp['name'] for emp in employees if emp['salary'] > 45000]
print(employees_name)


# third : Get only Development department employees.

employees_name = [emp['name'] for emp in employees if emp['department']=='Development' ]
print(employees_name)


# fourth : Create a dictionary of employee names and salaries.
employees_dict = {emp['name']:emp['salary'] for emp in employees}
print(employees_dict)


# five : Use map() to calculate yearly salaries

yearly_salaries = list(
    map(lambda employee: employee["salary"] * 12, employees)
)

print(yearly_salaries)


# sixth : Use filter() to find employees earning more than 50,000.

high_earners = list(
    filter(lambda employee: employee["salary"] > 50000, employees)
)
print(high_earners)


# Use lambda and sorted() to sort employees by salary.
sorted_employees = sorted(
    employees,
    key=lambda employee: employee["salary"]
)
print(sorted_employees)



#  seventh : Group employees by department.
grouped_employees = {}

for employee in employees:
    department = employee["department"]

    if department not in grouped_employees:
        grouped_employees[department] = []
    grouped_employees[department].append(employee["name"])

print(grouped_employees)


# 10. Average salary for each department
department_salary = {}

for employee in employees:

    department = employee["department"]
    salary = employee["salary"]

    if department not in department_salary:
        department_salary[department] = []

    department_salary[department].append(salary)


average_salary = {
    department: sum(salaries) / len(salaries)
    for department, salaries in department_salary.items()
}

print(average_salary)


# 11. Find second-highest distinct salary


unique_salaries = sorted(
    {employee["salary"] for employee in employees},
    reverse=True
)


if len(unique_salaries) >= 2:
    second_highest = unique_salaries[1]
    print(second_highest)
else:
    print("Second-highest salary not available")





