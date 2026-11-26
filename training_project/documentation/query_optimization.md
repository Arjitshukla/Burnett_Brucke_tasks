## Query Optimization – Trainer Dashboard

**Problem:**  
The trainer dashboard accessed each student's assigned courses and marks records inside a loop, which could result in N+1 database queries.

**Before Optimization:**  
Related courses and marks were fetched separately for each student.

**Optimization Applied:**  
Used `prefetch_related()` to fetch students' courses and CourseMarks records in bulk.

**After Optimization:**  
The optimized QuerySet uses:

```python
.prefetch_related('courses', 'course_marks__updated_by')
```

**Verification:**  
Tested with trainer ID 33, who has 16 assigned students and 2 courses.

The optimized QuerySet executed 4 SQL queries in the captured test.

**Result:**  
Reduced repeated database queries by fetching related records in bulk and avoiding N+1 query behaviour in the tested access pattern.