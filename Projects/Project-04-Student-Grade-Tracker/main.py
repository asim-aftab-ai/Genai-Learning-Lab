students = {}

while True:
    name = input("Enter student name (or type 'exit' to stop): ")
    
    if name == "exit":
        break
    
    grade = int(input("Enter grade: "))
    
    students[name] = grade

# Calculate average
total = 0

for grade in students.values():
    total += grade

average = total / len(students)

# Find top student
top_student = ""
top_grade = 0

for name, grade in students.items():
    if grade > top_grade:
        top_grade = grade
        top_student = name

# Output
print("\nAll Students:")
for name, grade in students.items():
    print(name, ":", grade)

print("\nAverage Grade:", average)
print("Top Student:", top_student, "-", top_grade)