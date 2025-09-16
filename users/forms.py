# from django import forms
# from django.contrib.auth.forms import AuthenticationForm

# class LoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'new-password'}),
        help_text="At least 8 characters; avoid common/fully numeric passwords."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'new-password'}),
        label="Confirm password"
    )
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name  = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email      = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'autofocus': True}),
        }

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('password')
        cpw = cleaned.get('confirm_password')
        if pwd and cpw and pwd != cpw:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        from .models import CustomUser
        user.role = CustomUser.Role.STUDENT  # self-registration defaults to Student
        if commit:
            user.save()
        return user
