from django.urls import path
from . import views

urlpatterns = [
    # --- Students ---
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:user_id>/', views.student_detail, name='student_detail'),
    path('students/<int:user_id>/update/', views.student_update, name='student_update'),
    path('students/<int:user_id>/delete/', views.student_delete, name='student_delete'),

    # --- Teachers ---
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:user_id>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:user_id>/delete/', views.teacher_delete, name='teacher_delete'),

    # --- Courses ---
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # --- Grades ---
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/create/', views.grade_create, name='grade_create'),
    path('grades/<int:pk>/update/', views.grade_update, name='grade_update'),
    path('grades/<int:pk>/delete/', views.grade_delete, name='grade_delete'),

    # --- Enrollment ---
    path('enroll/', views.enroll_student, name='enroll_student'),
]
