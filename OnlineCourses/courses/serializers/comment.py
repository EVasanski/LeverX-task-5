from rest_framework.serializers import ModelSerializer

from courses.models import CommentMark
from users.serializers import UserSerializer


class CommentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CommentMark
        fields = '__all__'


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = CommentMark
        fields = ('comment',)
