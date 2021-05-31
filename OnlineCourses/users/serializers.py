from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import User, Teacher, Student


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

    def to_representation(self, instance):
        return instance.username


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

    def to_representation(self, instance):
        return '{} {}'.format(instance.first_name, instance.last_name)


class StudentListSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        return '{} {}'.format(instance.first_name, instance.last_name)


