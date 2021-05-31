from django.urls import path

from .views.course import CourseListView, CourseDetailView, CourseAddUserView, CourseRemoveStudentView
from .views.lecture import LectureDetailView, LectureListView
from .views.homework import HomeworkView
from .views.solution import SolutionListView
from .views.mark import MarkView
from .views.comment import CommentListView


urlpatterns = [
    path('course/', CourseListView.as_view()),
    path('course/<int:course_pk>/', CourseDetailView.as_view()),
    path('course/<int:course_pk>/add-user/', CourseAddUserView.as_view()),
    path('course/<int:course_pk>/remove-student/', CourseRemoveStudentView.as_view()),
    path('course/<int:course_pk>/lectures/', LectureListView.as_view()),
    path('course/<int:course_pk>/lectures/<int:lecture_pk>/', LectureDetailView.as_view()),
    path('lectures/<int:lecture_pk>/homework/', HomeworkView.as_view()),
    path('lectures/<int:lecture_pk>/homework/solution/', SolutionListView.as_view()),
    path('homework/solution/<int:solution_pk>/', MarkView.as_view()),
    path('homework/solution/<int:solution_pk>/comments/', CommentListView.as_view()),

]
