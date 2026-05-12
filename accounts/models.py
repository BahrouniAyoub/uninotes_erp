from django.db import models
from config import settings


# Create your models here.
class Profile(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_TUTOR = 'tutor'
    
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'étudiant'),
        (ROLE_TUTOR, 'tuteur'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="tutors"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"