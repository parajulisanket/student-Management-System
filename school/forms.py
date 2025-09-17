from django import forms
from django.contrib.auth import get_user_model
from .models import StudentProfile, Course, Grade, Enrollment
from users.models import CustomUser

User = get_user_model()


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = StudentProfile
        fields = ['date_of_birth', 'address']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'description', 'assigned_teacher']  # include teacher

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only users with TEACHER role appear in the dropdown
        self.fields['assigned_teacher'].queryset = User.objects.filter(role=CustomUser.Role.TEACHER)
        self.fields['assigned_teacher'].required = False
        self.fields['assigned_teacher'].help_text = "Optional: pick the teacher responsible for this course."


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['enrollment', 'score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safer default ordering; teacher-specific filtering is done in the view
        self.fields['enrollment'].queryset = (
            Enrollment.objects.select_related('student', 'course')
            .order_by('course__code', 'student__username')
        )


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only students in the student dropdown
        self.fields['student'].queryset = User.objects.filter(role=CustomUser.Role.STUDENT).order_by('username')
        # Helpful ordering for courses; shows assigned teacher in labels via __str__ if you kept it
        self.fields['course'].queryset = Course.objects.select_related('assigned_teacher').order_by('code')
