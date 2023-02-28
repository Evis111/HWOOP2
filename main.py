class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades_lecturer:
                lecturer.grades_lecturer[course] += [grade]
            else:
                lecturer.grades_lecturer[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = sum(sum(self.grades.values(), [])) / len(sum(self.grades.values(), []))
        return f"Имя: {self.name}\nФамилия: {self.surname}\n" \
               f"Средняя оценка за домашние задания: {avg_grade:.1f}\n" \
               f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n" \
               f"Завершенные курсы: {', '.join(self.finished_courses)}"

    def __gt__(self, other):
        if isinstance(other, Student):
            return self.avg_grade() > other.avg_grade()
        else:
            return NotImplemented

    def avg_grade(self):
        return sum(sum(self.grades.values(), [])) / len(sum(self.grades.values(), []))

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = sum(sum(self.grades.values(), [])) / len(sum(self.grades.values(), []))
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade:.1f}'

    def __lt__(self, other):
        return self.avg_grade() < other.avg_grade()

    def avg_grade(self):
        return sum(sum(self.grades.values(), [])) / len(sum(self.grades.values(), []))


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

class Course:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

def create_courses(n):
    courses = []
    for i in range(n):
        name = input(f"Enter course name {i+1}: ")
        grade = float(input(f"Enter grade for {name}: "))
        course = Course(name, grade)
        courses.append(course)
    return courses

def calculate_average(courses, course_name):
    total = 0
    count = 0
    for course in courses:
        if course.name == course_name:
            total += course.grade
            count += 1
    if count == 0:
        return 0
    else:
        return total / count


# Создаем студентов
student_1 = Student('Ruoy', 'Eman', 'male')
student_1.courses_in_progress += ['Python']
student_1.finished_courses += ['Введение в программирование']
student_1.grades['Python'] = [10, 9, 8, 10]
student_1.grades['Введение в программирование'] = [9, 8, 9, 10]

student_2 = Student('Anna', 'Maria', 'female')
student_2.courses_in_progress += ['Git']
student_2.finished_courses += ['Введение в программирование']
student_2.grades['Git'] = [8, 7, 9, 10]
student_2.grades['Введение в программирование'] = [10, 10, 10, 10]

# Создаем лекторов
lecturer_1 = Lecturer('Vasya', 'Pupkin')
lecturer_1.courses_attached += ['Python']
lecturer_1.grades['Python'] = [10, 9, 10, 9]

lecturer_2 = Lecturer('Petya', 'Ivanov')
lecturer_2.courses_attached += ['Git']
lecturer_2.grades['Git'] = [9, 9, 9, 10]

# Создаем проверяющих
reviewer_1 = Reviewer('Sergey', 'Sidorov')
reviewer_1.courses_attached += ['Python']
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 8)
reviewer_1.rate_hw(student_2, 'Python', 7)

reviewer_2 = Reviewer('Ivan', 'Petrov')
reviewer_2.courses_attached += ['Git']
reviewer_2.rate_hw(student_2, 'Git', 9)
reviewer_2.rate_hw(student_2, 'Git', 8)
student_2.add_courses('Python')
print(student_1)
print(lecturer_1)
print(reviewer_1)

# Проверим сравнение экземпляров классов
print(student_1 > student_2)
print(lecturer_1 < lecturer_2)