from django.urls import path
from . import views
urlpatterns = [
    path('train/', views.train_model, name='train_model'),
    path('predict/<int:student_id>/', views.predict_student, name='predict_student'),
]
