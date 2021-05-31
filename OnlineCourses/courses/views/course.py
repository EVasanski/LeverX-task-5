from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from courses.permissions import IsTeacher, ReadOnly, IsCourseMember
from courses.serializers.course import CourseDetailSerializer, CourseListSerializer, CourseCreateSerializer
from users.models import Student
from users.serializers import UserSerializer, TeacherSerializer

User = get_user_model()


class CourseListView(ListCreateAPIView):
    permission_classes = [(IsAuthenticated & ReadOnly) | IsTeacher]
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [(IsCourseMember & ReadOnly) | (IsCourseMember & IsTeacher)]
    lookup_url_kwarg = 'course_pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseDetailSerializer
        return CourseCreateSerializer

    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs.get('course_pk'))


class CourseAddUserView(CreateAPIView):
    serializer_class = UserSerializer

    permission_classes = [IsTeacher & IsCourseMember]

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('course_pk'))
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('Пользователя с таким username или e-mail не существует', status=400)

        if user.is_teacher:
            course.teachers.add(user.teacher.id)
        else:
            course.students.add(user.student.id)
        return Response('{} "{}" успешно добавлен на курс'.format(user.get_role_display(), username), status=201)


class CourseRemoveStudentView(APIView):
    serializer_class = TeacherSerializer

    permission_classes = [IsTeacher & IsCourseMember]

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('course_pk'))
        username = request.data.get('username')

        try:
            student = course.students.get(user__username=username)
        except Student.DoesNotExist:
            return Response('Студент с таким username или e-mail в данном курсе не найден', status=400)

        course.students.remove(student)

        return Response('Студент "{}" успешно удален с курса'.format(username), status=201)
