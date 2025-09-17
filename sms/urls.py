from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('school/', include('school.urls')),
    path('predictor/', include('predictor.urls')),
]