import random

import factory
from django.core.management.base import BaseCommand
from django.db import transaction

from mock.factories import (
    CommentFactory,
    CourseFactory,
    GradeFactory,
    HomeWorkFactory,
    LectureFactory,
    SubmissionFactory,
    UserFactory,
)
from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission, User

# --- Определяем количество объектов для создания ---
NUM_STUDENTS = 1000
NUM_TEACHERS = 100
NUM_COURSES = 200
NUM_LECTURES = 1000
NUM_HOMEWORKS = 2000
NUM_SUBMISSIONS = 2000
NUM_GRADES = 1000
NUM_COMMENTS = 5000


class Command(BaseCommand):
    help = "Наполняет базу данных моковыми данными."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Удаление старых данных...")
        # Удаляем в обратном порядке создания, чтобы не нарушать внешние ключи
        models = [Comment, Grade, Submission, HomeWork, Lecture, Course]
        for m in models:
            m.objects.all().delete()
        # Удаляем только обычных пользователей, не трогая админов
        User.objects.filter(is_superuser=False, is_staff=False).delete()
        self.stdout.write(self.style.SUCCESS("Старые данные успешно удалены."))

        self.stdout.write("Создание новых данных...")

        # 1. Создаем пользователей
        self.stdout.write(f"Создание {NUM_STUDENTS} студентов и {NUM_TEACHERS} учителей...")
        students = UserFactory.create_batch(NUM_STUDENTS, role="STUDENT")
        teachers = UserFactory.create_batch(NUM_TEACHERS, role="TEACHER")
        all_users = students + teachers

        # 2. Создаем курсы
        self.stdout.write(f"Создание {NUM_COURSES} курсов...")
        courses = CourseFactory.create_batch(NUM_COURSES, author=factory.Iterator(teachers))

        # Назначаем учителей и студентов на курсы (связи ManyToMany)
        for course in courses:
            # Назначаем несколько случайных учителей
            course_teachers = random.sample(teachers, k=min(len(teachers), 3))
            # Назначаем 50 случайных студентов
            course_students = random.sample(students, k=min(len(students), 50))
            course.teachers.add(*course_teachers)
            course.students.add(*course_students)

        # 3. Создаем лекции
        self.stdout.write(f"Создание {NUM_LECTURES} лекций...")
        lectures = []
        # Чтобы данные были более реалистичными, лекцию должен вести учитель,
        # который назначен на данный курс.
        for _ in range(NUM_LECTURES):
            course = random.choice(courses)
            course_teachers = list(course.teachers.all())
            if not course_teachers:  # Если у курса нет учителей, берем любого
                course_teachers = teachers
            teacher = random.choice(course_teachers)
            lectures.append(LectureFactory(course=course, teacher=teacher))

        # 4. Создаем домашние задания
        self.stdout.write(f"Создание {NUM_HOMEWORKS} домашних заданий...")
        HomeWorkFactory.create_batch(
            NUM_HOMEWORKS,
            lecture=factory.Iterator(lectures),
        )
        homeworks = list(HomeWork.objects.all())

        # 5. Создаем решения (Submissions)
        self.stdout.write(f"Создание {NUM_SUBMISSIONS} решений...")
        submissions = SubmissionFactory.create_batch(
            NUM_SUBMISSIONS,
            homework=factory.Iterator(homeworks),
            author=factory.Iterator(students),
        )

        # 6. Создаем оценки (Grades)
        self.stdout.write(f"Создание {NUM_GRADES} оценок...")
        # У Grade связь OneToOne с Submission, поэтому нужно действовать аккуратно.
        # Оцениваем случайную выборку из созданных решений.
        submissions_to_grade = random.sample(submissions, k=min(NUM_GRADES, len(submissions)))
        grades = []
        for sub in submissions_to_grade:
            course_teachers = list(sub.homework.lecture.course.teachers.all())
            if not course_teachers:
                course_teachers = teachers
            grader = random.choice(course_teachers)
            grades.append(GradeFactory(submission=sub, author=grader))

        # 7. Создаем комментарии
        self.stdout.write(f"Создание {NUM_COMMENTS} комментариев...")
        if grades:
            CommentFactory.create_batch(
                NUM_COMMENTS,
                grade=factory.Iterator(grades),
                author=factory.Iterator(all_users),
            )

        self.stdout.write(self.style.SUCCESS("База данных успешно наполнена!"))
