import factory
from django.contrib.auth import get_user_model

from courses.models import Comment, Course, Grade, HomeWork, Lecture, Submission

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    role = "STUDENT"  # Default role

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        self.set_password("password123")
        self.save()


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Faker("sentence", nb_words=4)
    author = factory.SubFactory(UserFactory, role="TEACHER")


class LectureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lecture

    topic = factory.Faker("sentence", nb_words=3)
    datetime = factory.Faker("date_time_this_year")
    course = factory.SubFactory(CourseFactory)
    teacher = factory.SubFactory(UserFactory, role="TEACHER")


class HomeWorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HomeWork

    text = factory.Faker("paragraph", nb_sentences=5)
    lecture = factory.SubFactory(LectureFactory)
    author = factory.LazyAttribute(lambda obj: obj.lecture.teacher)


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Submission

    text = factory.Faker("paragraph", nb_sentences=3)
    author = factory.SubFactory(UserFactory, role="STUDENT")
    homework = factory.SubFactory(HomeWorkFactory)


class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grade

    submission = factory.SubFactory(SubmissionFactory)
    score = factory.Faker("random_int", min=1, max=100)
    author = factory.SubFactory(UserFactory, role="TEACHER")


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker("sentence", nb_words=10)
    grade = factory.SubFactory(GradeFactory)
    author = factory.SubFactory(UserFactory)
