from django.shortcuts import get_object_or_404
from rest_framework import permissions

from courses.models import Course, Lecture, Submission


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissions check if user is author of object.
    set `owner_field` where to orner of object should be.
    """
    message = 'You are not the owner of this object.'
    owner_field = 'author'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, self.owner_field) == request.user


class IsTeaacher(permissions.BasePermission):

    message = 'You are not a teacher.'

    def has_permission(self, request, view):
        return request.user.role == 'TEACHER'


class IsTeaacherOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    message = 'You are not a teacher.'

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or (
                request.user
                and request.user.is_authenticated
                and request.user.role == 'TEACHER'
            )
        )


class IsStudentrOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    message = 'You are not a student.'

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or (
                request.user
                and request.user.is_authenticated
                and request.user.role == 'STUDENT'
            )
        )


class CanAddLecture(permissions.BasePermission):

    message = 'You a not assigned to this course'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        course_id = view.kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)
        return bool(
            course.author == request.user
            or course.teachers.filter(id=request.user.id).exists()
        )


class CanAddHomeWork(permissions.BasePermission):

    message = 'You a not assigned to this lecture'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        lecture_id = view.kwargs['lecture_id']
        lecture = get_object_or_404(Lecture, id=lecture_id)
        return bool(
            lecture.teacher == request.user
        )


class CanAddReadComment(permissions.BasePermission):

    message = 'You a not assigned to this grade'

    def has_permission(self, request, view):
        if request.user.role == 'TEACHER':
            return True
        grade_id = view.kwargs.get('grade_id')
        submission = get_object_or_404(Submission, pk=grade_id)
        return bool(
            submission.author == request.user
        )


def get_owner_permission_class(field_name: str):
    """
    A factory function that creates a new permission class to check for object ownership.
    :param field_name: The name of the attribute on the object that contains the owner (User).
    """
    if not isinstance(field_name, str) or not field_name:
        raise ValueError("field_name must be a non-empty string.")

    class OwnerPermission(IsOwnerOrReadOnly):
        owner_field = field_name

    OwnerPermission.__name__ = f"IsOwnerVia{field_name.capitalize()}"
    return OwnerPermission
