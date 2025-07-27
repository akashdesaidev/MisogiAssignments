from collections import defaultdict
class Student:
    def __init__(self,id,name,email,stream) -> None:
        self.id=id
        self.name=name
        self.email=email
        self.stream=stream
        self.courses= dict()  

    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.stream},{(self.courses)})"

    def enroll_in_Course(self,course):
        self.courses[course.id]=course
        course.enroll_student(self)
        pass
    def add_grade(self,course_id,grade):
        if course_id in self.courses:
            self.courses[course_id].grades[self.id]=grade
        else:
            print(f"Student not enrolled in course: {course_id}")


class Course:
    total_enrollment=0
    def __init__(self,id,name,Tutor,capacity,duration) -> None:
        self.id=id
        self.name=name
        self.tutor=Tutor
        self.capacity=capacity
        self.duration=duration
        self.grades=defaultdict(float)
        self.enrolled=dict()
        self.waiting_list=[]
        

    @classmethod
    def increase_enrollment(cls):
     cls.total_enrollment+=1

    def __repr__(self):
        return f"Course({self.id}, {self.name}, Capacity: {self.capacity} course grades {self.grades})"
    
    def get_avaliable_spots(self):
        return self.capacity
    
    def enroll_student(self,student):
        if not self.isFull():
            self.enrolled[student.id]=student
            self.capacity-=1
            self.increase_enrollment()
        else:
            print("Course is alread Full")   

    def add_grades(self,stud_id,grades):
        if stud_id in self.enrolled:
            self.grades[stud_id]=grades
        else:
            print(f"Student not enrolled in course: {stud_id}")

    def isFull(self):
        return self.capacity<=0
    
math_course=Course("MATH_101","Calculus I","Dr.Smith",4,30)
physics_course=Course("PHYS_101","Caculus I","Dr.Smith",3,30)
cs_course=Course("CS_101","Calulus I","Dr.Smith",3,30)
# print(math_course.__dict__)
# print(math_course.get_avaliable_spots())
student1=Student("S001","Alice","Alice@gmail.com","Computer Science")
student2=Student("S002","Ali","Ali@gmail.com","Mathematics")
student3=Student("S003","Billu","Billu@gmail.com","Physics")
# print(studen1)
enrollment1=student1.enroll_in_Course(math_course)
enrollment1=student2.enroll_in_Course(math_course)
enrollment2=student1.enroll_in_Course(physics_course)
enrollment3=student3.enroll_in_Course(math_course)
# print(math_course.get_avaliable_spots())
student1.add_grade("MATH_101",85.5)
math_course.add_grades("S002",80.02)
# print(student1)
print(math_course.total_enrollment)
print(math_course.isFull())