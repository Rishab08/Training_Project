from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, User1
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone', 'date_of_birth', 'password', 'is_staff')


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User1
        fields = ('email', 'username', 'phone', 'picture', 'gender', 'date_of_birth', 'is_staff')


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User1
        fields = ('email', 'username', 'phone', 'date_of_birth', 'picture','gender', 'password', 'is_active')


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone', 'date_of_birth', 'is_staff', 'is_superuser')


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone', 'date_of_birth', 'password', 'is_active', 'is_superuser')
