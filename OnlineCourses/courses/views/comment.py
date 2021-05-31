from rest_framework.generics import ListCreateAPIView

from courses.models import CommentMark, SolutionMark
from courses.permissions import IsSolutionAuthor, IsTeacher, IsCourseMember
from courses.serializers.comment import CommentSerializer, CommentCreateSerializer


class CommentListView(ListCreateAPIView):
    permission_classes = [(IsCourseMember & IsTeacher) | IsSolutionAuthor]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        return CommentCreateSerializer

    def get_queryset(self):
        solution = self.kwargs.get('solution_pk')
        return CommentMark.objects.filter(mark__solution_id=solution)

    def perform_create(self, serializer):
        mark = SolutionMark.objects.get(solution_id=self.kwargs.get('solution_pk'))
        serializer.save(user=self.request.user, mark=mark)
