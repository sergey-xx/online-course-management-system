import random

import factory
from django.core.management.base import BaseCommand
from django.db import transaction

from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission, User
from mock.factories import (
    CommentFactory,
    CourseFactory,
    GradeFactory,
    HomeWorkFactory,
    LectureFactory,
    SubmissionFactory,
    UserFactory,
)

NUM_STUDENTS = 1000
NUM_TEACHERS = 100
NUM_COURSES = 200
NUM_LECTURES = 1000
NUM_HOMEWORKS = 2000
NUM_SUBMISSIONS = 2000
NUM_GRADES = 1000
NUM_COMMENTS = 5000


class Command(BaseCommand):
    help = "Fills the database with mock data."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        models = [Comment, Grade, Submission, HomeWork, Lecture, Course]
        for m in models:
            m.objects.all().delete()
        User.objects.filter(is_superuser=False, is_staff=False).delete()
        self.stdout.write(self.style.SUCCESS("Old data has been successfully deleted."))

        self.stdout.write("Creating new data...")

        self.stdout.write(f"Creating {NUM_STUDENTS} students and {NUM_TEACHERS} teachers...")
        students = UserFactory.create_batch(NUM_STUDENTS, role="STUDENT")
        teachers = UserFactory.create_batch(NUM_TEACHERS, role="TEACHER")
        all_users = students + teachers

        self.stdout.write(f"Creating {NUM_COURSES} courses...")
        courses = CourseFactory.create_batch(NUM_COURSES, author=factory.Iterator(teachers))

        for course in courses:
            course_teachers = random.sample(teachers, k=min(len(teachers), 3))
            course_students = random.sample(students, k=min(len(students), 50))
            course.teachers.add(*course_teachers)
            course.students.add(*course_students)

        self.stdout.write(f"Creating {NUM_LECTURES} lectures...")
        lectures = []
        for _ in range(NUM_LECTURES):
            course = random.choice(courses)  # NOQA: S311
            course_teachers = list(course.teachers.all())
            if not course_teachers:
                course_teachers = teachers
            teacher = random.choice(course_teachers)  # NOQA: S311
            lectures.append(LectureFactory(course=course, teacher=teacher))

        self.stdout.write(f"Creating {NUM_HOMEWORKS} homworks...")
        HomeWorkFactory.create_batch(
            NUM_HOMEWORKS,
            lecture=factory.Iterator(lectures),
        )
        homeworks = list(HomeWork.objects.all())

        self.stdout.write(f"Crerating {NUM_SUBMISSIONS} submissions...")
        submissions = SubmissionFactory.create_batch(
            NUM_SUBMISSIONS,
            homework=factory.Iterator(homeworks),
            author=factory.Iterator(students),
        )

        self.stdout.write(f"Creating {NUM_GRADES} grades...")
        submissions_to_grade = random.sample(submissions, k=min(NUM_GRADES, len(submissions)))
        grades = []
        for sub in submissions_to_grade:
            course_teachers = list(sub.homework.lecture.course.teachers.all())
            if not course_teachers:
                course_teachers = teachers
            grader = random.choice(course_teachers)  # NOQA: S311
            grades.append(GradeFactory(submission=sub, author=grader))

        self.stdout.write(f"Creating {NUM_COMMENTS} comments...")
        if grades:
            CommentFactory.create_batch(
                NUM_COMMENTS,
                grade=factory.Iterator(grades),
                author=factory.Iterator(all_users),
            )

        self.stdout.write(self.style.SUCCESS("The database has been successfully filled!"))
