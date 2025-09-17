# from django.contrib.auth.views import LoginView
# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
# from django.contrib import messages
# from .forms import LoginForm
# from .models import CustomUser

# class LoginViewCustom(LoginView):
#     template_name = 'users/login.html'
#     authentication_form = LoginForm

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# @login_required
# def dashboard(request):
#     user = request.user
#     if user.role == CustomUser.Role.ADMIN:
#         return render(request, 'users/admin_dashboard.html')
#     elif user.role == CustomUser.Role.TEACHER:
#         return render(request, 'users/teacher_dashboard.html')
#     else:
#         return render(request, 'users/student_dashboard.html')

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import LoginForm, SignupForm
from .models import CustomUser

class LoginViewCustom(LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. You can now log in.')
            return redirect('login')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    if user.role == CustomUser.Role.ADMIN:
        return render(request, 'users/admin_dashboard.html')
    elif user.role == CustomUser.Role.TEACHER:
        return render(request, 'users/teacher_dashboard.html')
    else:
        return render(request, 'users/student_dashboard.html')