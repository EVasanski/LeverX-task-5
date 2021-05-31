from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView

from courses.models import Homework, HomeworkSolution
from courses.permissions import IsCourseMember, IsStudent, ReadOnly
from courses.serializers.solution import SolutionSerializer, SolutionCreateSerializer


class SolutionListView(ListCreateAPIView):
    permission_classes = [(IsCourseMember & ReadOnly) | (IsCourseMember & IsStudent)]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SolutionSerializer
        return SolutionCreateSerializer

    def get_queryset(self):
        homework = get_object_or_404(Homework, lecture_id=self.kwargs.get('lecture_pk'))
        user = self.request.user
        if user.is_teacher:
            return HomeworkSolution.objects.filter(homework=homework)
        return HomeworkSolution.objects.filter(Q(homework=homework) & Q(student=user.student))

    def perform_create(self, serializer):
        homework = get_object_or_404(Homework, lecture_id=self.kwargs.get('lecture_pk'))
        student = self.request.user.student
        serializer.save(homework=homework, student=student)
