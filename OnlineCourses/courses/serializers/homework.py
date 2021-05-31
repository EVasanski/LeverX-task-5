from rest_framework.serializers import ModelSerializer, ValidationError

from courses.models import Homework


class HomeworkSerializer(ModelSerializer):
    class Meta:
        model = Homework
        fields = ('task', 'created')
    #
    # def validate(self, attrs):
    #
    #     if Homework.objects.filter(lecture=attrs['lecture']).exists():
    #         raise ValidationError('Homework already exists')


