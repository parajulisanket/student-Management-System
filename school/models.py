from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"StudentProfile<{self.user}>"

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return f"{self.code} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('student', 'course')
    def __str__(self):
        return f"{self.student} in {self.course}"

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    score = models.FloatField(help_text='0-100')
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.enrollment} -> {self.score}"
