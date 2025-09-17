from django.contrib import admin
from .models import StudentProfile, Course, Enrollment, Grade


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "address")
    search_fields = ("user__username", "user__first_name", "user__last_name", "address")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "assigned_teacher")
    search_fields = ("code", "title", "assigned_teacher__username")
    list_filter = ("assigned_teacher",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course")
    search_fields = ("student__username", "course__code", "course__title")
    list_filter = ("course",)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "score", "date")
    list_filter = ("date", "enrollment__course")
    search_fields = ("enrollment__student__username", "enrollment__course__code")
