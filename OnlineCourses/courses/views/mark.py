from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import ListCreateAPIView

from courses.models import HomeworkSolution
from courses.permissions import IsCourseMember, IsTeacher, IsSolutionAuthor, ReadOnly
from courses.serializers.mark import MarkSerializer
from courses.serializers.solution import SolutionSerializer


class MarkView(ListCreateAPIView):
    permission_classes = [(IsCourseMember & IsTeacher) | (IsSolutionAuthor & ReadOnly)]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SolutionSerializer
        return MarkSerializer

    def get_queryset(self):
        return get_list_or_404(HomeworkSolution, pk=self.kwargs.get('solution_pk'))

    def perform_create(self, serializer):
        solution = get_object_or_404(HomeworkSolution, pk=self.kwargs.get('solution_pk'))
        return serializer.save(solution=solution)
