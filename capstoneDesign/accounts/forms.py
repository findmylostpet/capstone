from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(ModelForm):
    #username = forms.CharField()
    #email = forms.CharField()
    #password = forms.CharField(widget=forms.PasswordInput)
    passwordCheck = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    phone = forms.CharField()

    fieldOrder=['username', 'email', 'password','password_check','phone']

    class Meta:
        model=User
        widgets = {'password' : forms.PasswordInput}
        fields = ('username','email', 'password','phone')

class LoginForm(ModelForm):
    class Meta:
        model = User
        widgets = {'password' : forms.PasswordInput}
        fields = ('email','password')
