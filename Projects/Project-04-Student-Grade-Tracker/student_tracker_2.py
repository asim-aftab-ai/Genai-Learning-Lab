grades = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78
}

grades["Diana"] = 95
total_score = sum(grades.values())
student_count = len(grades)
average_score = total_score / student_count
print("class average: " + str(average_score))

top_student = ""
highest_score = -1

for name, score in grades.items():
    if score > highest_score:
        highest_score = score
        top_student = name

print("Top Student:", top_student, "with a score of", highest_score)
