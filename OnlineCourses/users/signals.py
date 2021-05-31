from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Teacher, Student


@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_teacher:
            Teacher.objects.create(user=instance,
                                   first_name=instance.first_name,
                                   last_name=instance.last_name,
                                   email=instance.email)


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            Student.objects.create(user=instance,
                                   first_name=instance.first_name,
                                   last_name=instance.last_name,
                                   email=instance.email)
