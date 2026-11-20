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
# =====================================================================

# Feature 6: Closure (NATIVE in Python)
def make_curve(points, cap=100):
    """Outer function ('curve maker') that returns a closure."""
    def apply_curve(mark):
        # Retains `points` and `cap` even after make_curve() returns
        return min(mark + points, cap)
    return apply_curve


# Task 2 Requirement: Recursive subprogram (NATIVE in Python)
def total_marks_recursive(marks, index=0):
    """Recursively calculates a student's total marks.
    Used in the report and for Task 2 Stack Diagram #2."""
    if index == len(marks):             # Base case
        return 0
    current = marks[index]              # Local variable in this activation record
    rest_total = total_marks_recursive(marks, index + 1)
    return current + rest_total


# Feature 7: Generator / Semi-Coroutine (NATIVE in Python)
# Note: This is a generator (produces values via `yield`), not a full
# coroutine (which also receives values via `.send()`).
def report_generator(student_list):
    """Yields one student's report at a time, suspending execution
    and preserving local state between calls."""
    for idx, s in enumerate(student_list, 1):
        total = total_marks_recursive(s.marks)
        avg = s.average()
        status = "PASS" if avg >= 50 else "FAIL"
        yield (
            f"[{idx}/{len(student_list)}] {s.name:<8} | "
            f"Marks: {s.marks} | Total: {total} | Avg: {avg:5.1f} | {status}"
        )


def option_curve_marks():
    """Menu option 5 - Feature 6 (Closure), ready to pair with M4's Feature 5."""
    try:
        points = int(input("Enter curve points to add (e.g. 5): "))
    except ValueError:
        print("Points must be a whole number.")
        return

    curve_fn = make_curve(points)       # Outer function returns; closure persists

    # NOTE FOR M4 INTEGRATION:
    # Once M4 finishes Feature 5 (e.g. apply_to_all(students, func)),
    # replace the loop below with M4's higher-order function call.
    for s in students:
        s.marks = [curve_fn(m) for m in s.marks]

    print(f"Applied +{points} curve (capped at 100) to all students.")
    show_students()


def option_report():
    """Menu option 6 - Feature 7 (Generator, pauses on Enter)."""
    gen = report_generator(students)
    print("\n--- Student Performance Report ---")
    for i, line in enumerate(gen, 1):
        print(line)
        if i < len(students):
            input("Press Enter for next student...")
    print("--- End of Report ---")


def demo_m5():
    """Non-interactive demo of Features 6, 7 and recursion. (M5)"""
    # Feature 6: Closure
    curve_plus_5 = make_curve(5)
    print("Closure (85 -> +5):", curve_plus_5(85))
    print("Closure (98 -> +5, capped):", curve_plus_5(98))

    # Feature 7: Generator (manual next() calls show suspend/resume without input())
    gen = report_generator(students)
    print("Generator yield 1:", next(gen))
    print("Generator yield 2:", next(gen))
    print("Generator yield 3:", next(gen))

    # Task 2: Recursive call
    ali_marks = students[0].marks       # [70, 85, 60]
    total = total_marks_recursive(ali_marks)
    print(f"Recursive total for {students[0].name} {ali_marks}: {total}")


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
