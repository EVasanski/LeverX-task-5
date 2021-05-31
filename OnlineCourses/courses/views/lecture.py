from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from courses.models import Lecture, Course
from courses.permissions import IsCourseMember, IsTeacher, ReadOnly
from courses.serializers.lecture import LectureDetailSerializer, LectureCreateSerializer


class LectureListView(ListCreateAPIView):
    serializer_class = LectureDetailSerializer

    permission_classes = [(IsCourseMember & ReadOnly) | (IsCourseMember & IsTeacher)]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LectureCreateSerializer
        return LectureDetailSerializer

    def get_queryset(self):
        return Lecture.objects.filter(course_id=self.kwargs.get('course_pk'))

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs.get('course_pk'))
        serializer.save(course=course)


class LectureDetailView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'lecture_pk'
    permission_classes = [(IsCourseMember & ReadOnly) | (IsCourseMember & IsTeacher)]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LectureDetailSerializer
        return LectureCreateSerializer

    def get_queryset(self):
        return Lecture.objects.filter(course_id=self.kwargs.get('course_pk'))
