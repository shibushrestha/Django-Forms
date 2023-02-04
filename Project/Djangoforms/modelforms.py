# We will use the 'User' model form django.contrib.auth.models for ModelFormPractice

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder':"Confirm password"}), required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':"Enter a username"})
        self.fields['email'].widget.attrs.update({'placeholder':"Enter a email address"})
        self.fields['email'].required = True
        self.fields['password'].widget.attrs.update({'placeholder':"Enter password"})

    class Meta:
        model = User
        fields = ("username", "email", "password",)
      
        widgets = {
            'password' : forms.PasswordInput
        }
        error_messages={
            'username':{
                'unique':"Username already taken.",
            },
            
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError(_("Please enter same passwords."), code="password_mismatch")

