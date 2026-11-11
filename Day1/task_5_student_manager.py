import json
import os

Students ={}

# step 1 :Add a new student to the dictionary

def add_student( ):
    name = input("Enter student name: ").strip().title()
    if not name:
        print("Student name cannot be empty!")
        return
    if name in Students:
        print("Student already exists!")
        return
    marks = {}
    for subject in ["Python", "SQL", "Django"]:
        while True:
            try:
                mark = float(input(f"Enter marks for {subject}: ")).split()
                if not mark:
                    print("Marks cannot be empty. Please enter a value.")
                    continue    

                if 0 <= mark <= 100:
                    marks[subject] = mark
                    break
                else:
                    print("Marks should be between 0 and 100. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    Students[name] = marks
    print(f"Student {name} added successfully!")



# Step 3: Update Marks

def update_marks():
    name = input("Enter student name to update marks: ").strip().title()
    if name not in Students:
        print("Student not found!")
        return
    subject = input("Enter subject name (Python, SQL, Django):").strip().title()

    # check if the subject is available for the Student
    if subject not in Students[name]:
        print("Invalid subject!")
        return
    while True:
        try:
            new_mark = float(input(f"Enter new marks for {subject}: "))
            if 0 <= new_mark <= 100:
                Students[name][subject] = new_mark
                print(f"Marks for {subject} updated successfully!")
                break
            else:
                print("Marks should be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")



# step 4: Delete a student from the dictionary

def delete_student():
    name = input("Enter student name to delete: ").strip().title()
    if name in Students:
        del Students[name]
        print(f"Student {name} deleted successfully!")
    else:
        print("Student not found!")



# Step 5: View All Students


def view_all_students():
    if not Students:
        print("No students found.")
        return

    for name, marks in Students.items():
        print(f"Student Name: {name}")
        for subject, mark in marks.items():
            print(f"  {subject}: {mark}")
        print()  


#step 6:  search by name

def search_student():
    name = input("Enter student name to search: ").strip().title()
    if name in Students:
        print(f"Student Name: {name}")
        for subject, mark in Students[name].items():
            print(f"  {subject}: {mark}")
    else:
        print("Student not found!")


# step 7:Calculate Total and Average

def calculate_total_and_average():
    name = input("Enter student name to calculate total and average: ").strip().title()

    if name in Students:
        total = sum(Students[name].values())
        average = total / len(Students[name])
        print(f"Total Marks for {name}: {total}")
        print(f"Average Marks for {name}: {average:.2f}%")
    else:
        print("Student not found!")



# step 8: Display Pass or Fail

def display_pass_or_fail():
    name = input("Enter student name to check pass or fail: ").strip().title()

    if name in Students:
        marks = Students[name]

        if not marks:
            print("No marks available for this student.")
            return
        
        if all(mark >= 40 for mark in marks.values()):
            print(f"{name} has passed.")
            
        else:
            print(f"{name} has failed.")
    else:
        print("Student not found!")


# step 9:Display the highest-scoring student.

def display_highest_scoring_student():
    if not Students:
        print("No students found.")
        return
    total = {
        name: sum(marks.values())
        for name, marks in Students.items()
    }
    highest_student = max(total, key=total.get)
    print(f"The highest-scoring student is {highest_student} with a total of {total[highest_student]} marks.")



def load_data():
    global Students

    if os.path.exists("students.json"):
        try:
            with open("students.json", "r") as file:
                Students = json.load(file)

            if not isinstance(Students, dict):
                print("Invalid JSON data format!")
                Students = {}

        except (json.JSONDecodeError, OSError):
            print("Unable to load student data!")
            Students = {}
    else:
        Students = {}


# Step 2: Save data to JSON file

def save_data():
    with open("students.json", "w") as file:
        json.dump(Students, file, indent=4)


# Lets connect all the functions to a menu-driven program


def main():
    load_data()
    while True:
        print("\n===Student Management System ==")
        print("1. Add Student")
        print("2. Update Marks")
        print("3. Delete Student")
        print("4. View All Students")
        print("5. Search Student")
        print("6. Calculate Total and Average")
        print("7. Display Pass or Fail")
        print("8. Display Highest Scoring Student")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            add_student()
        elif choice == '2':
            update_marks()
        elif choice == '3':
            delete_student()
        elif choice == '4':
            view_all_students()
        elif choice == '5':
            search_student()
        elif choice == '6':
            calculate_total_and_average()
        elif choice == '7':
            display_pass_or_fail()
        elif choice == '8':
            display_highest_scoring_student()
        elif choice == '9':
            save_data()
            print("Exiting the program.")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
