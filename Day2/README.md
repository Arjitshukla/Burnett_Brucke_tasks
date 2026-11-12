# Day 2 Tasks

Python practice scripts for Day 2 of the internship.

## Files

- `task_1_advanced_functions.py` - advanced functions: argument handling (`*args`, `**kwargs`), salary validation, execution-time decorator, salary statistics, and a closure for running totals.
- `task_2_file_handling.py` - menu-based Employee Management System using `employees.json` for storage (add, display, search, update, delete, count).
- `task_3_data_processing.py` - data processing on in-memory employee records using list/dict comprehensions, `map()`, `filter()`, `sorted()`, grouping, and aggregations.
- `employees.json` - sample/working employee data for Task 2.

## Run

From this `Day2` directory:

```powershell
python task_1_advanced_functions.py
python task_2_file_handling.py
python task_3_data_processing.py
```

Or from the workspace root:

```powershell
python Day2\task_1_advanced_functions.py
python Day2\task_2_file_handling.py
python Day2\task_3_data_processing.py
```

## Notes

- Requires Python 3.
- Task 2 reads/writes `employees.json` from the current working directory; run it from the directory where that file is available (workspace root in this setup).
