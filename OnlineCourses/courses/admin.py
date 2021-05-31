from django.contrib import admin

from .models import Course, Lecture, Homework, HomeworkSolution, SolutionMark, CommentMark

# Register your models here.
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Homework)
admin.site.register(HomeworkSolution)
admin.site.register(SolutionMark)
admin.site.register(CommentMark)
