from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from users.models import CustomUser
from .models import StudentProfile, Course, Grade, Enrollment
from .forms import StudentForm, CourseForm, GradeForm, EnrollmentForm

User = get_user_model()

@login_required
def student_list(request):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    students = User.objects.filter(role=CustomUser.Role.STUDENT).select_related('student_profile')
    return render(request, 'school/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = User.objects.create_user(username=username, password=password, role=CustomUser.Role.STUDENT,
                                        first_name=first_name or '', last_name=last_name or '', email=email or '')
        form = StudentForm(request.POST, user_instance=user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Student created.')
            return redirect('student_list')
        else:
            user.delete()
            messages.error(request, 'Fix errors in profile form.')
    else:
        form = StudentForm()
    return render(request, 'school/student_form.html', {'form': form, 'create': True})

@login_required
def student_detail(request, user_id):
    if request.user.role not in [CustomUser.Role.ADMIN, CustomUser.Role.TEACHER] and request.user.id != user_id:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard')
    student = get_object_or_404(User, pk=user_id, role=CustomUser.Role.STUDENT)
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    grades = Grade.objects.filter(enrollment__student=student).select_related('enrollment__course')
    return render(request, 'school/student_detail.html', {
        'student': student, 'enrollments': enrollments, 'grades': grades,
    })

@login_required
def student_update(request, user_id):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    student = get_object_or_404(User, pk=user_id, role=CustomUser.Role.STUDENT)
    profile = getattr(student, 'student_profile', None) or StudentProfile(user=student)
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name', student.first_name)
        student.last_name = request.POST.get('last_name', student.last_name)
        student.email = request.POST.get('email', student.email)
        student.save()
        form = StudentForm(request.POST, instance=profile, user_instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=profile, user_instance=student)
    return render(request, 'school/student_form.html', {'form': form, 'student': student, 'create': False})

@login_required
def student_delete(request, user_id):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    student = get_object_or_404(User, pk=user_id, role=CustomUser.Role.STUDENT)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted.')
        return redirect('student_list')
    return render(request, 'school/student_confirm_delete.html', {'student': student})

@login_required
def course_list(request):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    courses = Course.objects.all()
    return render(request, 'school/course_list.html', {'courses': courses})

@login_required
def course_create(request):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'school/course_form.html', {'form': form, 'create': True})

@login_required
def course_update(request, pk):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'school/course_form.html', {'form': form, 'create': False})

@login_required
def course_delete(request, pk):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('course_list')
    return render(request, 'school/course_confirm_delete.html', {'course': course})

@login_required
def grade_list(request):
    if request.user.role not in [CustomUser.Role.TEACHER, CustomUser.Role.ADMIN]:
        messages.error(request, 'Teachers or Admin only.')
        return redirect('dashboard')
    grades = Grade.objects.select_related('enrollment__student', 'enrollment__course')
    return render(request, 'school/grade_list.html', {'grades': grades})

@login_required
def grade_create(request):
    if request.user.role not in [CustomUser.Role.TEACHER, CustomUser.Role.ADMIN]:
        messages.error(request, 'Teachers or Admin only.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade added.')
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'school/grade_form.html', {'form': form, 'create': True})

@login_required
def grade_update(request, pk):
    if request.user.role not in [CustomUser.Role.TEACHER, CustomUser.Role.ADMIN]:
        messages.error(request, 'Teachers or Admin only.')
        return redirect('dashboard')
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated.')
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'school/grade_form.html', {'form': form, 'create': False})

@login_required
def grade_delete(request, pk):
    if request.user.role not in [CustomUser.Role.TEACHER, CustomUser.Role.ADMIN]:
        messages.error(request, 'Teachers or Admin only.')
        return redirect('dashboard')
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted.')
        return redirect('grade_list')
    return render(request, 'school/grade_confirm_delete.html', {'grade': grade})

@login_required
def enroll_student(request):
    if request.user.role != CustomUser.Role.ADMIN:
        messages.error(request, 'Admins only.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student enrolled in course.')
            return redirect('student_list')
    else:
        form = EnrollmentForm()
    return render(request, 'school/grade_form.html', {'form': form, 'create': True})
