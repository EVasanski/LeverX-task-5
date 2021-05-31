from rest_framework.serializers import ModelSerializer, StringRelatedField

from courses.models import HomeworkSolution
from courses.serializers.mark import MarkSerializer


class SolutionSerializer(ModelSerializer):
    mark = MarkSerializer(source='related_mark')
    student = StringRelatedField()
    homework = StringRelatedField()

    class Meta:
        model = HomeworkSolution
        fields = '__all__'


class SolutionCreateSerializer(ModelSerializer):
    class Meta:
        model = HomeworkSolution
        fields = ('solution',)
