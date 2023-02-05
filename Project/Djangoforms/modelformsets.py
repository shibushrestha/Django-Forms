from django.forms import modelformset_factory
from .models import Student
from .modelforms import UserRegistrationForm

UserProfileFormset = modelformset_factory(Student, fields="__all__")