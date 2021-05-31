from django.db.models import Q
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Course, HomeworkSolution


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsSolutionAuthor(BasePermission):
    def has_permission(self, request, view):
        try:
            solution = HomeworkSolution.objects.get(pk=view.kwargs.get('solution_pk'))
        except HomeworkSolution.DoesNotExist:
            return False
        if request.user.is_authenticated and request.user.is_student and solution.student == request.user.student:
            return True
        return False


class IsCourseMember(BasePermission):
    def has_permission(self, request, view):
        course = view.kwargs.get('course_pk', False)
        lecture = view.kwargs.get('lecture_pk', False)
        solution = view.kwargs.get('solution_pk', False)
        try:
            course = Course.objects.get(Q(pk=course) |
                                        Q(related_lectures__id=lecture) |
                                        Q(related_lectures__related_homework__related_homework_solutions__id=solution))
        except Course.DoesNotExist:
            return False

        if course.students.filter(user_id=request.user.id).exists():
            return True
        elif course.teachers.filter(user_id=request.user.id).exists():
            return True
        else:
            return False
