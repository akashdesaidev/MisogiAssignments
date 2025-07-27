from collections import defaultdict

class GradeManager:
    def __init__(self):
        self.grades = defaultdict(list)

    def add_grades(self, student_name, subject, grade):
        self.grades[student_name].append((subject, grade))
        return True

    def get_average(self, student_name):
        if not self.grades[student_name]:
            return "Student not found"
        
        total = sum(mark for _, mark in self.grades[student_name])
        average = total / len(self.grades[student_name])
        return round(average, 2)

    def get_subject_statistics(self, subject):
        sub_marks = [
            mark
            for subjects in self.grades.values()
            for subj, mark in subjects
            if subj == subject
        ]

        if not sub_marks:
            return f"No data found for subject: {subject}"

        statistic = {
            "average": round(sum(sub_marks) / len(sub_marks), 2),
            "marks": sub_marks,
            "lowest": min(sub_marks),
            "highest": max(sub_marks),
            "student_count": len(sub_marks)
        }
        return statistic

    def get_top_students(self, n=3):
        student_averages = [
            (student, sum(mark for _, mark in data) / len(data))
            for student, data in self.grades.items()
            if data  # avoid division by zero
        ]
        top_students = sorted(student_averages, key=lambda x: x[1], reverse=True)[:n]
        return [(name, round(avg, 2)) for name, avg in top_students]

    def get_failing_students(self, passing_grade=60):
        failing_students = []

        for student, data in self.grades.items():
            if not data:
                continue
            avg = sum(mark for _, mark in data) / len(data)
            if avg < passing_grade:
                failing_students.append((student, round(avg, 2)))

        return failing_students


# Sample Data
grades_data = [
    ("John", "Math", 85), ("John", "Science", 90), ("John", "English", 78),
    ("Jane", "Math", 92), ("Jane", "Science", 88), ("Jane", "English", 95),
    ("Jim", "Math", 75), ("Jim", "Science", 80), ("Jim", "English", 85), ("Jim", "History", 50),
    ("Jill", "Math", 85), ("Jill", "Science", 90), ("Jill", "English", 88), ("Jill", "History", 82),
    ("Jill", "Art", 95), ("Jill", "Music", 85), ("Ji", "Music", 58), ("Ji", "Musi", 58),
    ("Jill", "Physical Education", 90),
]

# Usage
grade_manager = GradeManager()
for student, subject, grade in grades_data:
    grade_manager.add_grades(student, subject, grade)

print("Average of John:", grade_manager.get_average("John"))
print("\nScience Stats:", grade_manager.get_subject_statistics("Science"))
print("\nFailing Students:", grade_manager.get_failing_students())
print("\nTop Students:", grade_manager.get_top_students(5))
