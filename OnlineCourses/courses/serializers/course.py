from rest_framework.serializers import ModelSerializer, StringRelatedField

from courses.models import Course
from .lecture import LectureListSerializer


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description')

    def create(self, validated_data):
        user = validated_data.pop('user')
        course = Course.objects.create(**validated_data)
        course.teachers.add(user.teacher)
        return course


class CourseDetailSerializer(ModelSerializer):
    lectures = LectureListSerializer(source='related_lectures', many=True, required=False)
    teachers = StringRelatedField(many=True, required=False)
    students = StringRelatedField(many=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'
        # depth = 1


class CourseListSerializer(CourseDetailSerializer):

    def to_representation(self, instance):
        return 'id {} : {}'.format(instance.id, instance.title)
