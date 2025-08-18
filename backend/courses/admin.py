from django.contrib import admin

from .models import Comment, Course, HomeWork, Lecture, Submission


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ...


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    ...


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    ...


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    ...


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...
