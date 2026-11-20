"""
WIF3010 Tutorial 4 - Student Grade System
Shared skeleton. Each member fills in ONLY their own section.

HOW THIS WORKS
- The Student class, the sample `students` list, menu() and demo() are shared.
- Each member owns one MENU HANDLER and one DEMO function (named in their
  section). menu() and demo() already call these, so do NOT rename them.
- Inside your section you are free to write ANY functions you like to
  showcase your feature, as long as they fit the Student Grade System.
- Do NOT rename Student, .name, .marks, .average() or `students`.
- Label each function with the feature it shows and whether it is
  NATIVE or SIMULATED in Python.
- Run `python grades.py` before sending your code to M1.

Owners:
  M1 - Student class, Feature 8, menu(), demo(), helpers
  M2 - Feature 1, Feature 2
  M3 - Feature 3
  M4 - Feature 4, Feature 5
  M5 - Feature 6, Feature 7, recursive call for Task 2
"""


# =====================================================================
# SHARED DATA + FEATURE 8: User-defined overloaded operators  (M1)
# =====================================================================
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks              # list of ints, e.g. [70, 85, 60]

    def average(self):
        return sum(self.marks) / len(self.marks) if self.marks else 0

    # Feature 8: s1 + s2 -> merged record (NATIVE operator overloading)
    def __add__(self, other):
        return Student(f"{self.name}&{other.name}", self.marks + other.marks)

    # Feature 8: s1 < s2 -> compare by average (lets sorted() rank students)
    def __lt__(self, other):
        return self.average() < other.average()

    def __repr__(self):
        return f"Student({self.name}, {self.marks})"


students = [
    Student("Ali", [70, 85, 60]),
    Student("Mei", [90, 75, 88]),
    Student("Raj", [55, 65, 72]),
]


# =====================================================================
# M2 - FEATURE 1: Subprogram definitions and parameters
#      FEATURE 2: Local referencing environments
# Menu: 1. Add student, 2. View all students & grades
# Must show: formal/actual params, default values, return values,
#            positional + keyword args; local variables, nested
#            functions, variable lifetime.
# =====================================================================

def option_add_student():
    """Menu option 1. (M2)"""
    print("TODO (M2): add a student")


def option_view_students():
    """Menu option 2. (M2)"""
    show_students()                     # replace/extend as you like
    print("TODO (M2): show grades")


def demo_m2():
    """Non-interactive demo of Features 1 and 2. (M2)"""
    print("TODO (M2)")


# =====================================================================
# M3 - FEATURE 3: Parameter-passing modes and methods
# Menu: 3. Adjust marks  (+ an "out" example in option 4 if you want)
# Must show: in / out / inout modes; pass-by-value, pass-by-result,
#            pass-by-value-result, pass-by-reference. Label which are
#            native and which are simulated.
# =====================================================================

def option_adjust_marks():
    """Menu option 3. (M3)"""
    print("TODO (M3): adjust marks")


def demo_m3():
    """Non-interactive demo of Feature 3. (M3)"""
    print("TODO (M3)")


# =====================================================================
# M4 - FEATURE 4: Overloaded and generic subprograms
#      FEATURE 5: Subprograms as parameters and indirect calls
# Menu: 4. Show class statistics  (Feature 5 is used by option 5 too)
# Must show: overloaded + generic functions; a function that takes
#            another function as a parameter and calls it indirectly.
# =====================================================================

def option_statistics():
    """Menu option 4. (M4)"""
    print("TODO (M4): class statistics")


def demo_m4():
    """Non-interactive demo of Features 4 and 5. (M4)"""
    print("TODO (M4)")


# =====================================================================
# M5 - FEATURE 6: Closures
#      FEATURE 7: Coroutines or generators
#      + a RECURSIVE call for the Task 2 stack diagram
# Menu: 5. Curve all marks, 6. Generate report
# Must show: a closure that keeps its variables after the outer
#            function returns; a generator/coroutine that suspends and
#            resumes. Coordinate with M4 if option 5 uses their
#            function-as-parameter code.
# =====================================================================

def option_curve_marks():
    """Menu option 5. (M5, with M4's Feature 5)"""
    print("TODO (M5): curve all marks")


def option_report():
    """Menu option 6. (M5)"""
    print("TODO (M5): generate report")


def demo_m5():
    """Non-interactive demo of Features 6, 7 and recursion. (M5)"""
    print("TODO (M5)")


# =====================================================================
# M1 - FEATURE 8 menu options + HELPERS + MENU + DEMO
# =====================================================================

def show_students():
    """Shared helper: list students with their marks and average."""
    for i, s in enumerate(students, 1):
        print(f"{i}. {s.name:<10} marks={s.marks} avg={s.average():.1f}")


def pick_student(prompt="Choose student number: "):
    """Shared helper: let the user choose a student; returns Student or None."""
    show_students()
    try:
        return students[int(input(prompt)) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return None


def read_marks(prompt="Enter marks separated by spaces: "):
    """Shared helper: read a list of int marks; returns list or None."""
    try:
        return [int(x) for x in input(prompt).split()]
    except ValueError:
        print("Marks must be whole numbers.")
        return None


def option_rank_students():
    """Menu option 7 - Feature 8 (<)."""
    for rank, s in enumerate(sorted(students, reverse=True), 1):
        print(f"{rank}. {s.name} avg={s.average():.1f}")


def option_merge_students():
    """Menu option 8 - Feature 8 (+)."""
    a = pick_student("First student: ")
    b = pick_student("Second student: ")
    if a and b and a is not b:
        print("Merged:", a + b)


def demo_m1():
    """Non-interactive demo of Feature 8."""
    print(students[0] + students[1])          # __add__
    print(students[0] < students[1])          # __lt__
    print([s.name for s in sorted(students, reverse=True)])


def menu():
    options = {
        "1": ("Add student", option_add_student),
        "2": ("View all students & grades", option_view_students),
        "3": ("Adjust marks", option_adjust_marks),
        "4": ("Show class statistics", option_statistics),
        "5": ("Curve all marks", option_curve_marks),
        "6": ("Generate report", option_report),
        "7": ("Rank students", option_rank_students),
        "8": ("Merge two student records", option_merge_students),
    }
    while True:
        print("\n===== Student Grade System =====")
        for key, (label, _) in options.items():
            print(f"{key}. {label}")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Bye!")
            break
        elif choice in options:
            options[choice][1]()
        else:
            print("Invalid option.")


def demo():
    """Runs every feature without input(), for Python Tutor / OneCompiler."""
    print("=== Features 1 & 2 (M2) ===");      demo_m2()
    print("=== Feature 3 (M3) ===");           demo_m3()
    print("=== Features 4 & 5 (M4) ===");      demo_m4()
    print("=== Features 6, 7 & recursion (M5) ==="); demo_m5()
    print("=== Feature 8 (M1) ===");           demo_m1()


if __name__ == "__main__":
    # demo()        # use this for Python Tutor screenshots
    menu()      # uncomment for the interactive system
