from itertools import chain

from django.contrib.auth import get_user_model
from django.db import models

from users.models import Teacher, Student

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    teachers = models.ManyToManyField(Teacher,
                                      verbose_name='Преподаватель/и',
                                      related_name='related_course',
                                      blank=True)
    students = models.ManyToManyField(Student,
                                      verbose_name='Студент/ы',
                                      related_name='related_course',
                                      blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def members(self):
        return list(chain(self.teachers.all(), self.students.all()))

    @property
    def lectures(self):
        return self.related_lectures.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lecture(models.Model):
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE, related_name='related_lectures')
    title = models.CharField(max_length=255, verbose_name='Тема')
    description = models.CharField(max_length=255, verbose_name='Описание', blank=True)
    presentation = models.FileField(verbose_name='Презентация', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def homework(self):
        return self.related_homework

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class Homework(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE, related_name='related_homework')
    task = models.TextField(verbose_name='Задание')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def homework_solutions(self):
        return self.related_homework_solutions.all()

    def __str__(self):
        return '{} : {}'.format(self.lecture.course.title, self.lecture.title)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'


class HomeworkSolution(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='related_homework_solutions',
                                 blank=True, null=True)
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE, blank=True, null=True)
    solution = models.FileField(verbose_name='Решение')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def mark(self):
        return self.related_mark

    def __str__(self):
        return '{} : {}'.format(self.student, self.homework)

    class Meta:
        verbose_name = 'Решение домашнего задания'
        verbose_name_plural = 'Решения домашних заданий'


class SolutionMark(models.Model):
    solution = models.OneToOneField(HomeworkSolution, related_name='related_mark', on_delete=models.CASCADE, blank=True)
    mark = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def comments(self):
        return self.related_comments.all()

    def __str__(self):
        return '{}'.format(self.mark)

    class Meta:
        verbose_name = 'Отметка за домашнее задание'
        verbose_name_plural = 'Отметки за домашнее задания'


class CommentMark(models.Model):
    mark = models.ForeignKey(SolutionMark, related_name='related_comments', on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, related_name='related_user', on_delete=models.CASCADE, blank=True)
    comment = models.TextField(verbose_name='Комментарий к заданию')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.mark, self.user)

    class Meta:
        verbose_name = 'Комментарий к домашнему заданию'
        verbose_name_plural = 'Комментарии к домашним заданиям'
