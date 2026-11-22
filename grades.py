"""
WIF3010 Tutorial 4 - Student Grade System

Owners:
  M1 - Student class, Feature 8, menu(), demo(), helpers
  M2 - Feature 1, Feature 2
  M3 - Feature 3
  M4 - Feature 4, Feature 5
  M5 - Feature 6, Feature 7, recursive call for Task 2
"""

from functools import singledispatch
from typing import Callable, List, Optional, TypeVar

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

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


#FEATURE 1:
#create_student() builds a new Student, a list of marks and an optional bonus (default 0), and returns it.
#option_add_student() reads the input, calls create_student()
#returned Student to the `students` list. 

def create_student(name, marks, bonus=0):
    """Build a Student. Every mark gets `bonus` extra points (capped at 100).
    The caller's `marks` list is NOT modified (a new list is built)."""
    boosted = [min(m + bonus, 100) for m in marks]    # local variable
    return Student(name, boosted)


def option_add_student():
    """Menu option 1 - Feature 1: Add a student. (M2)"""
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    marks = read_marks("Enter marks (0-100) separated by spaces: ")
    if not marks:
        print("At least one mark is required.")
        return
    if any(m < 0 or m > 100 for m in marks):
        print("Marks must be between 0 and 100.")
        return

    bonus_text = input("Bonus points for every mark (Enter = 0): ").strip()
    try:
        bonus = int(bonus_text) if bonus_text else 0
    except ValueError:
        print("Bonus must be a whole number.")
        return

    if bonus_text:
        new_student = create_student(name, marks, bonus)         
    else:
        new_student = create_student(name=name, marks=marks)     # keyword args, default bonus=0
    students.append(new_student)
    print(f"Added: {new_student}")
    
    
#FEATURES 2:
# works out a student's total, average
def compute_grade(student, pass_mark=50):
    """Return (total, average, letter) for one student."""
    total = sum(student.marks)                                  # local
    average = total / len(student.marks) if student.marks else 0  # local

    def to_letter(score):                       # nested helper
        if score < pass_mark:                   # reads parent's variable
            return "F"
        if score >= 80:
            return "A"
        if score >= 70:
            return "B"
        if score >= 60:
            return "C"
        return "D"

    grade = to_letter(average)                  # local
    return total, average, grade
    # <- on return: total, average, grade, to_letter and the frame are destroyed


def option_view_students():
    """Menu option 2 - Feature 2: View all students and their grades. (M2)"""
    if not students:
        print("No students yet.")
        return
    print(f"\n{'#':<3}{'Name':<10}{'Marks':<20}{'Total':>6}{'Avg':>8}  Grade")
    for i, s in enumerate(students, 1):
        total, average, grade = compute_grade(s)
        print(f"{i:<3}{s.name:<10}{str(s.marks):<20}{total:>6}{average:>8.1f}  {grade}")

#shows that the locals and the nested function no longer exist after the call returns.
def demo_m2():
    """Non-interactive demo of Features 1 and 2. (M2)"""
    # ---- Feature 1: parameters, defaults, return values ----
    print("[F1] positional args  :", create_student("Siti", [60, 70, 80], 5))
    print("[F1] keyword args     :", create_student(marks=[60, 70, 80], name="Siti"))
    print("[F1] default bonus=0  :", create_student("Siti", [60, 70, 80]))
    print("[F1] cap at 100       :", create_student("Top", [98, 100], bonus=10))

    # ---- Feature 2: local variables, nested function, lifetime ----
    ali = students[0]                                  # Student("Ali", [70, 85, 60])
    total, average, grade = compute_grade(ali)         # frame created here
    print(f"[F2] {ali.name}: total={total}, average={average:.1f}, grade={grade}")
    print("[F2] stricter pass_mark=75 :", compute_grade(ali, pass_mark=75)[2])

    # Lifetime: compute_grade's frame is gone, so its local names no longer exist.
    try:
        print(to_letter(90))                            # nested helper is not visible here
    except NameError as err:
        print("[F2] lifetime ended   :", err)


# FEATURE 3:
# in / out / inout modes; pass-by-value, pass-by-result,
# pass-by-value-result, pass-by-reference.

# 1. Mode: IN | Method: Pass-by-value
# Status in Python: NATIVE-EQUIVALENT for immutable types (int, float, str)
def preview_adjusted_mark(mark, bonus):
    """Caller -> Subprogram only. Rebinding `mark` locally does NOT
    change the caller's variable."""
    mark = min(mark + bonus, 100)       # modifies local binding only
    return mark


# 2. Mode: OUT | Method: Pass-by-result
# Status in Python: SIMULATED (using a mutable dict populated only at exit)
def compute_mark_summary(marks, out_summary):
    """Subprogram -> Caller only. Ignores initial contents of `out_summary`
    and writes results back only at the end of the subprogram."""
    if not marks:
        result = {"min": 0, "max": 0, "avg": 0.0}
    else:
        result = {
            "min": min(marks),
            "max": max(marks),
            "avg": round(sum(marks) / len(marks), 1),
        }
    # Copy-out at the end of execution
    out_summary.clear()
    out_summary.update(result)


# 3. Mode: INOUT | Method: Pass-by-value-result (copy-in, copy-out)
# Status in Python: SIMULATED (using a 1-element list as a mutable box)
def adjust_mark_value_result(mark_box, bonus):
    """Caller <-> Subprogram. Copies value IN at start, works on a local
    copy, and copies value OUT to caller's box only at the end."""
    local_mark = mark_box[0]            # Copy-in at start
    local_mark = max(0, min(local_mark + bonus, 100))
    # Notice: mark_box[0] is still unchanged until the line below
    mark_box[0] = local_mark            # Copy-out at end


# 4. Mode: INOUT | Method: Pass-by-reference
# Status in Python: NATIVE-EQUIVALENT for mutable objects (list, Student)
def apply_bonus_by_ref(student, index, bonus):
    """Caller <-> Subprogram. Mutates the caller's Student object in-place
    through its object reference; changes are visible immediately."""
    student.marks[index] = max(0, min(student.marks[index] + bonus, 100))


def option_adjust_marks():
    """Menu option 3 - Feature 3: Adjust a student's mark. (M3)"""
    student = pick_student("Choose student to adjust: ")
    if not student or not student.marks:
        return

    print(f"Current marks for {student.name}:")
    for i, m in enumerate(student.marks, 1):
        print(f"  {i}. {m}")

    try:
        idx = int(input("Choose mark number to adjust: ")) - 1
        if not (0 <= idx < len(student.marks)):
            print("Invalid mark number.")
            return
        bonus = int(input("Enter points to add/subtract (e.g. 5 or -5): "))
    except ValueError:
        print("Please enter whole numbers.")
        return

    # Demonstrate IN (pass-by-value) to preview without changing data
    preview = preview_adjusted_mark(student.marks[idx], bonus)
    print(f"Preview (pass-by-value, original unchanged): "
          f"{student.marks[idx]} -> {preview}")

    confirm = input("Apply this change? (y/n): ").strip().lower()
    if confirm == "y":
        # Demonstrate INOUT (pass-by-reference) to update in-place
        apply_bonus_by_ref(student, idx, bonus)

        # Demonstrate OUT (pass-by-result) to retrieve updated summary
        summary = {}
        compute_mark_summary(student.marks, summary)
        print(f"Updated {student.name}: marks={student.marks} | "
              f"min={summary['min']}, max={summary['max']}, avg={summary['avg']}")
    else:
        print("Adjustment cancelled.")


def demo_m3():
    """Non-interactive demo of Feature 3 for Python Tutor / OneCompiler. (M3)"""
    # Use a dedicated Student instance so we don't alter shared `students` for M5
    demo_student = Student("Ali_Demo", [70, 85, 60])

    # 1. IN mode — Pass-by-value (NATIVE-EQUIVALENT for int)
    original_mark = demo_student.marks[0]
    preview = preview_adjusted_mark(original_mark, 10)
    print(f"[IN / Pass-by-value] preview={preview}, "
          f"caller original_mark={original_mark} (unchanged)")

    # 2. OUT mode — Pass-by-result (SIMULATED)
    summary_out = {}
    compute_mark_summary(demo_student.marks, summary_out)
    print(f"[OUT / Pass-by-result] summary_out={summary_out}")

    # 3. INOUT mode — Pass-by-value-result (SIMULATED)
    mark_box = [demo_student.marks[2]]          # [60]
    adjust_mark_value_result(mark_box, 8)
    print(f"[INOUT / Pass-by-value-result] mark_box after call={mark_box}")

    # 4. INOUT mode — Pass-by-reference (NATIVE-EQUIVALENT for mutable Student)
    print(f"[INOUT / Pass-by-reference] before: {demo_student}")
    apply_bonus_by_ref(demo_student, 0, 5)
    print(f"[INOUT / Pass-by-reference] after:  {demo_student}")


T = TypeVar("T")


# Feature 4a: Overloaded subprogram (SIMULATED in Python via singledispatch)
@singledispatch
def summarize(data):
    """Default fallback if an unsupported type is passed."""
    return f"Unsupported data type: {type(data).__name__}"


@summarize.register(Student)
def _(student: Student):
    """Overload 1: summarize a single Student object."""
    return (
        f"Student {student.name}: marks={student.marks}, "
        f"avg={student.average():.1f}"
    )


@summarize.register(list)
def _(items: list):
    """Overload 2: summarize a list of Students or a list of numeric marks."""
    if not items:
        return "Empty list."
    if isinstance(items[0], Student):
        class_avg = sum(s.average() for s in items) / len(items)
        return f"Class of {len(items)} students | Overall Avg: {class_avg:.1f}"
    return (
        f"{len(items)} marks | Min: {min(items)}, "
        f"Max: {max(items)}, Avg: {sum(items) / len(items):.1f}"
    )


@summarize.register(int)
@summarize.register(float)
def _(mark):
    """Overload 3: summarize a single numeric mark."""
    status = "PASS" if mark >= 50 else "FAIL"
    return f"Single mark: {mark} ({status})"


# Feature 4b: Generic subprogram (NATIVE via dynamic typing / duck typing,
#             with static TypeVar annotations from Python's typing module)
def find_highest(
    items: List[T],
    key_fn: Callable[[T], float]
) -> Optional[T]:
    """Generic function that returns the highest item of any type T,
    using key_fn to extract a comparable numeric score."""
    if not items:
        return None
    best = items[0]
    best_score = key_fn(best)
    for item in items[1:]:
        score = key_fn(item)
        if score > best_score:
            best = item
            best_score = score
    return best


# Feature 5: Subprograms as parameters and indirect calls (NATIVE in Python)
def compute_class_stat(
    student_list: List[Student],
    stat_fn: Callable[[List[float]], float]
) -> float:
    """Accepts a statistic function (stat_fn) as a parameter and invokes it
    indirectly on the list of student averages."""
    if not student_list:
        return 0.0
    averages = [s.average() for s in student_list]
    return stat_fn(averages)            # Indirect call to passed function


def apply_to_all(
    student_list: List[Student],
    mark_fn: Callable[[int], int]
) -> None:
    """Higher-order function (Feature 5) used by M5's option_curve_marks().
    Accepts a transformation function and calls it indirectly on every mark."""
    for s in student_list:
        s.marks = [mark_fn(m) for m in s.marks]     # Indirect call


def _mean(values: List[float]) -> float:
    """Helper statistic function passed to compute_class_stat()."""
    return sum(values) / len(values)


def option_statistics():
    """Menu option 4 - Features 4 & 5. (M4)"""
    if not students:
        print("No students available.")
        return

    print("\n--- Class Statistics ---")
    # Feature 4a: Overloaded summarize() with different argument types
    print(summarize(students))                      # list[Student]
    all_marks = [m for s in students for m in s.marks]
    print(summarize(all_marks))                     # list[int]

    # Feature 4b: Generic find_highest() on Student objects and int marks
    top_student = find_highest(students, lambda s: s.average())
    highest_mark = find_highest(all_marks, lambda m: m)
    print("Top Student ->", summarize(top_student)) # Student overload
    print("Highest Mark ->", summarize(highest_mark))  # int overload

    # Feature 5: Indirect calls via compute_class_stat()
    print(f"Class Mean Avg:    {compute_class_stat(students, _mean):.1f}")
    print(f"Highest Avg:       {compute_class_stat(students, max):.1f}")
    print(f"Lowest Avg:        {compute_class_stat(students, min):.1f}")


def demo_m4():
    """Non-interactive demo of Features 4 and 5. (M4)"""
    # Feature 4a: Overloaded function (singledispatch)
    print("Overload (Student):", summarize(students[0]))
    print("Overload (list):   ", summarize(students))
    print("Overload (int):    ", summarize(88))

    # Feature 4b: Generic function (same function works on Student, int, str)
    top_s = find_highest(students, lambda s: s.average())
    top_m = find_highest([70, 85, 60], lambda m: m)
    longest_name = find_highest(["Ali", "Mei", "Rajesh"], len)
    print(f"Generic (Student): {top_s.name} ({top_s.average():.1f})")
    print(f"Generic (int):     {top_m}")
    print(f"Generic (str):     {longest_name}")

    # Feature 5: Subprograms as parameters & indirect calls
    print(f"Indirect call (mean): {compute_class_stat(students, _mean):.1f}")
    print(f"Indirect call (max):  {compute_class_stat(students, max):.1f}")

    # Demo apply_to_all() on a temporary student so shared `students` stays
    # unchanged for M5's demo_m5()
    sample = [Student("Demo", [60, 80])]
    apply_to_all(sample, lambda m: min(m + 5, 100))
    print("Indirect call (apply_to_all +5):", sample[0])


# Feature 6: Closure (NATIVE in Python)
def make_curve(points, cap=100):
    """Outer function ('curve maker') that returns a closure."""
    def apply_curve(mark):
        # Retains `points` and `cap` even after make_curve() returns
        return min(mark + points, cap)
    return apply_curve


# Task 2: Recursive subprogram (NATIVE in Python)
def total_marks_recursive(marks, index=0):
    """Recursively calculates a student's total marks.
    Used in the report and for Task 2 Stack Diagram #2."""
    if index == len(marks):             # Base case
        return 0
    current = marks[index]              # Local variable in this activation record
    rest_total = total_marks_recursive(marks, index + 1)
    return current + rest_total


# Feature 7: Generator / Semi-Coroutine (NATIVE in Python)
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

    apply_to_all(students, curve_fn)

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
    menu()      
