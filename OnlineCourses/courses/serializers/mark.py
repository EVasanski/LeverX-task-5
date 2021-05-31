from rest_framework.serializers import ModelSerializer

from courses.models import SolutionMark
from .comment import CommentSerializer


class MarkSerializer(ModelSerializer):
    comments = CommentSerializer(source='related_comments', many=True, required=False)

    class Meta:
        model = SolutionMark
        fields = ('mark', 'comments')

    def create(self, validated_data):
        solution = validated_data.get('solution')
        if SolutionMark.objects.filter(solution=solution).exists():
            mark = SolutionMark.objects.get(solution=solution)
            mark.mark = validated_data.get('mark')
            mark.save()
        else:
            mark = SolutionMark.objects.create(**validated_data)
        return mark
