from django.contrib import admin

from .models import Comment, Course, Grade, HomeWork, Lecture, Submission


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ...


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'topic',
        'teacher',
        'presentation_file',
        'datetime',
    )


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    ...


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    ...


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    ...
