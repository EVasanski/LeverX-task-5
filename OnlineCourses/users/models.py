from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    USER_ROLES = (
        ('teacher', 'Преподаватель'),
        ('student', 'Студент')
    )

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(verbose_name='Роль', max_length=30, choices=USER_ROLES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role']

    # objects = CustomUserManager()

    def __str__(self):
        return '{} : {}'.format(self.username, self.get_role_display())

    @property
    def is_teacher(self):
        if self.role == 'teacher':
            return True
        else:
            return False

    @property
    def is_student(self):
        if self.role == 'student':
            return True
        else:
            return False


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='student', null=False)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)

    @property
    def courses(self):
        return self.related_course.all()

    def __str__(self):
        return '{} : {} {}'.format(self.user.username, self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='teacher', null=False)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)

    @property
    def courses(self):
        return self.related_course.all()

    def __str__(self):
        return '{} : {} {}'.format(self.user.username, self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
