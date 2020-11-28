from django import forms
from django.forms import ModelForm

class ProfileForm(forms.Form):
    photo = forms.ImageField()



    