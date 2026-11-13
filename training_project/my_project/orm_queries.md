## 1. Get all students
```python
from students.models import Student, Department, Course, StudentProfile
from django.db.models import Q, Avg, Max, Min, Count
```
**Requirement:** Get all students from the database.

**ORM Query:**
```python
Student.objects.all()
```
***Output:**
'harsh yadav'
'priya ravat'
'shreya'
'jhone'
'Deepak'
'Aman'
'Riya'
'Rahul'
'Neha'
'Priya'

**Description:** 
## all() ##
:  Use to retrive all object from perticular model. and also its return Queryset


## 2. Get only active students
```python
from students.models import Student, Department, Course, StudentProfile
from django.db.models import Q, Avg, Max, Min, Count
```
**Requirement:** Get all Active students from the database.

**ORM Query:**
```python
Student.objects.filter(is_active=True)
```
***Output:**
'harsh yadav'
'shreya'
'jhone'
'Deepak'
'Aman'
'Riya'
'Rahul'
'Neha'
'Priya'

**Description:** 
## Filter() ##
:  it is only use for filtering based on a conditions and above Query return only active Student.




## 3.Get students whose marks are greater than or equal to 60

```python
from students.models import Student, Department, Course, StudentProfile

from django.db.models import Q, Avg, Max, Min, Count
```
**Requirement:** Get students whose marks are greater than or equal to 60 by useing **__gte**

**ORM Query:**
```python
Student.objects.filter(marks__gte = 60)
```
***Output:**
'harsh yadav'
'shreya'
'jhone'
'Deepak'
'Aman'
'Riya'
'Rahul'
'Neha'
'Priya'

**Description:** 
## gte ##
: gte  is the lookup method which means Greater Than or Equal To.



## 4. Students whose names contain a given word

```python
from students.models import Student, Department, Course, StudentProfile

from django.db.models import Q, Avg, Max, Min, Count
```
**Requirement:** Students whose names contain a given word

**ORM Query:**
```python
Student.objects.filter(name__icontains="Aman")
```
***Output:**
<QuerySet [<Student: Aman>]>

**Description:** 
## icontains ##
: icontains case-insensitive can seach . Example: Aman, aman, AMAN.





## 5. Get top three students by marks


**Requirement:** get top three students

**ORM Query:**
```python
Student.objects.order_by("-marks")[:3]
```
***Output:**
<QuerySet [<Student: Priya>, <Student: Rahul>, <Student: Deepak>]>


## 6. Order students by marks


**Requirement:** get data into Marks ascending order

**ORM Query:**
```python
Student.objects.order_by("marks")
```
***Output:**
<QuerySet [<Student: harsh yadav>, <Student: jhone>, <Student: shreya>, <Student: priya ravat>, <Student: Aman>, <Student: Riya>, <Student: Neha>, <Student: Deepak>, <Student: Rahul>, <Student: Priya>]>



## 6. Order students by marks


**Requirement:** get student in  ascending order

**ORM Query:**
```python
Student.objects.order_by("marks")
```
***Output:**
<QuerySet [<Student: harsh yadav>, <Student: jhone>, <Student: shreya>, <Student: priya ravat>, <Student: Aman>, <Student: Riya>, <Student: Neha>, <Student: Deepak>, <Student: Rahul>, <Student: Priya>]>





## 7. Get students from a specific department


**Requirement:** department__name accesses the related Department model's name field.

**ORM Query:**
```python
Student.objects.filter(department__name="Python Development")
```
***Output:**
<QuerySet [<Student: shreya>, <Student: jhone>, <Student: Aman>, <Student: Neha>]>



## 8. Get students enrolled in a specific course


**Requirement:**Filters students enrolled in course code PY101. distinct() prevents duplicate students.

**ORM Query:**
```python
Student.objects.filter(courses__code="PY101").distinct()
```
***Output:**
<QuerySet [<Student: jhone>, <Student: Deepak>, <Student: Aman>, <Student: Neha>]>



## 9 Get all courses for one student


**Requirement:**Returns all courses associated with Aman through the ManyToMany relationship.
**ORM Query:**
```python

student = Student.objects.get(name="Aman")
student.courses.all()

```
***Output:**
<QuerySet [<Course: Python Programming (PY101)>, <Course: Django Development (DJ201)>]>




## 10. Count total students


**ORM Query:**
```python

Student.objects.count()

```
***Output:**
10


## 11. Calculate average marks


**ORM Query:**
```python
Student.objects.aggregate(average_marks=Avg("marks"))

```
***Output:**
{'average_marks': 63.9}

**Explanation**: aggregate() calculates an overall value. Avg() calculates the average marks.




## 12. Get highest and lowest marks


**ORM Query:**
```python
Student.objects.aggregate(
    highest_marks=Max("marks"),
    lowest_marks=Min("marks")
)

```
***Output:**
{'average_marks': 63.9}

**Explanation**: aggregate() calculates an overall value. Avg() calculates the average marks.


## 13. Count students in each department.


**ORM Query:**
```python
Department.objects.annotate(
    student_count=Count("students")
)
```
### To display department names with student counts:

```python
for department in Department.objects.annotate(student_count=Count("students")):
    print(department.name, department.student_count)

```
***Output:**
Python Development 4
Web Development 3
Data Science 3

**Explanation**: annotate() adds a calculated field to each Department object.






## 14. Find departments with more than three students


**ORM Query:**
```python
Department.objects.annotate(
    student_count=Count("students")
).filter(student_count__gt=3)


```
***Output:**
{'average_marks': 63.9}

**Explanation**: gt means greater than. This returns departments having more than three students.


## 15. Find students who do not have a profile


**ORM Query:**
```python
Student.objects.filter(profile__isnull=True)
```
***Output:**
<QuerySet [<Student: harsh yadav>, <Student: priya ravat>, <Student: shreya>, <Student: jhone>, <Student: Deepak>]>

**Explanation:** :Finds students for whom the reverse OneToOne relationship profile does not exist.


## 16. Find students enrolled in more than one course


**ORM Query:**
```python
Student.objects.annotate(
    course_count=Count("courses")
).filter(course_count__gt=1)
```
***Output:**
<QuerySet [<Student: shreya>, <Student: jhone>, <Student: Aman>, <Student: Neha>, <Student: priya ravat>, <Student: Riya>, <Student: Priya>,<Student: harsh yadav>, <Student: Deepak>]>

**Explanation:** :Counts courses for every student and returns students having more than one course.



## 17. Search students by name or email using Q objects

**ORM Query:**
```python
Student.objects.filter(
    Q(name__icontains="aman") |
    Q(email__icontains="aman")
)
```
***Output:**
<QuerySet [<Student: Aman>]>

**Explanation:** :Explanation:
- Q() allows complex conditions.
- | means OR.
- icontains performs a case-insensitive search.






## 18. Update inactive students to active using update()
First check inactive students:

**ORM Query:**
```python
Student.objects.filter(is_active=False)
```

Count them:

```python
Student.objects.filter(is_active=False).count()
```

Then update:

```python
Student.objects.filter(is_active=False).update(is_active=True)

```

**Explanation**: update() updates multiple database records directly without calling each model's save() method.






## 19. Delete records with invalid marks, if any


### First identify invalid records:
**ORM Query:**
```python
Student.objects.filter(
    Q(marks__lt=0) | Q(marks__gt=100)
)
```
### Count them:

```python
Student.objects.filter(
    Q(marks__lt=0) | Q(marks__gt=100)
).count()
```

### If invalid records exist and you have verified them, delete:

```python
Student.objects.filter(
    Q(marks__lt=0) | Q(marks__gt=100)
).delete()
```

**Explanation:** Deletes students whose marks are below 0 or above 100.
Important: Always inspect records before deleting.

# 20. Use select_related() and prefetch_related() appropriately
```python
students = Student.objects.select_related(
    "department"
).prefetch_related("courses")

```

Display student, department, and courses:
```python
for student in students:
    print(student.name)
    print(student.department)
    print(list(student.courses.all()))
```
## **1. Difference between&#x20;**`select_related()`**&#x20;and&#x20;**`prefetch_related()`

| `select_related()`                              | `prefetch_related()`                                |
| ----------------------------------------------- | --------------------------------------------------- |
| Used for ForeignKey and OneToOne relationships. | Used for ManyToMany and reverse relationships.      |
| Fetches related objects using SQL JOIN.         | Fetches related objects using separate SQL queries. |
| Retrieves data in a single SQL query.           | Retrieves data using multiple SQL queries.          |
| Best for single-valued relationships.           | Best for multi-valued relationships.                |
| Example: Student → Department                   | Example: Student → Courses                          |
| `Student.objects.select_related("department")`  | `Student.objects.prefetch_related("courses")`       |

## **2. Difference between&#x20;**`aggregate()`**&#x20;and&#x20;**`annotate()`

| `aggregate()`                                                   | `annotate()`                                                    |
| --------------------------------------------------------------- | --------------------------------------------------------------- |
| Calculates summary values for the entire queryset.              | Calculates values for each object in the queryset.              |
| Returns a dictionary.                                           | Returns queryset objects with additional calculated fields.     |
| Does not return individual model objects.                       | Returns individual model objects along with calculated fields.  |
| Used for overall calculations.                                  | Used for per-object calculations.                               |
| Example: Average marks of all students.                         | Example: Number of students in each department.                 |
| `Student.objects.aggregate(Avg("marks"))`                       | `Department.objects.annotate(Count("students"))`                |
| Common functions: `Avg()`, `Max()`, `Min()`, `Count()`, `Sum()` | Common functions: `Avg()`, `Max()`, `Min()`, `Count()`, `Sum()` |