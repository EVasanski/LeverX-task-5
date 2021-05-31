from rest_framework.serializers import ModelSerializer

from courses.models import Lecture
from .homework import HomeworkSerializer


class LectureCreateSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('title', 'description', 'presentation')


class LectureDetailSerializer(ModelSerializer):
    homework = HomeworkSerializer(source='related_homework')

    class Meta:
        model = Lecture
        fields = '__all__'


class LectureListSerializer(LectureDetailSerializer):
    def to_representation(self, instance):
        return 'id {} : {}'.format(instance.id, instance.title)
