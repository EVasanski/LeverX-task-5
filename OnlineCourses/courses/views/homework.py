from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView

from courses.models import Homework, Lecture
from courses.permissions import IsCourseMember, IsTeacher, ReadOnly
from courses.serializers.homework import HomeworkSerializer


class HomeworkView(ListCreateAPIView):
    permission_classes = [(IsCourseMember & ReadOnly) | (IsCourseMember & IsTeacher)]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        return Homework.objects.filter(lecture_id=self.kwargs.get('lecture_pk'))

    def perform_create(self, serializer):
        lecture = get_object_or_404(Lecture, pk=self.kwargs.get('lecture_pk'))
        serializer.save(lecture=lecture)
