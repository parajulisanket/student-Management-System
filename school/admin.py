from django.contrib import admin
from .models import StudentProfile, Course, Enrollment, Grade
admin.site.register(StudentProfile)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Grade)
