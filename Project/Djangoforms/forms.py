from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator, RegexValidator

# You can write custom validators like this:
# This can be usesful when you to apply custom logic for validation.
# This validator checks the uniqueness of username with respect to the User model.
def unique_username(value):
    if value and User.objects.filter(username=value).exists():
        raise ValidationError(_('Username already taken.'), code="unique")

# Using the built-in RegexValidator to only allow the following character in the username
username_validator = RegexValidator(r'^[A-Za-z0-9.#!@$]*$', 
    message="Only alphanumeric characters and .#!@$ is allowed in the username", code="invalid")


class UserRegisterForm(forms.Form):
    
    username = forms.CharField(max_length=100,
        required=True,
        # You can use validators in the form field same as in model field like so:
        validators = [unique_username, username_validator],
        # You can override the default error_messages in form field like so:
        error_messages={
            'required':'You must enter a username.'
        },
        # You can define widget for the form field and add attributes like so:
        widget=forms.TextInput(attrs={
            'placeholder':'Enter a username'
        })
    )
    first_name = forms.CharField(max_length=100,
        required=True,
            error_messages={
        'required':'This field must be filled out.'
        },
        widget=forms.TextInput(attrs={
            'placeholder':'Enter your first name'
        })
    )
    last_name = forms.CharField(max_length=100,
        required=True,
        error_messages={
            'required':'This field must be filled out.'
        },
        widget=forms.TextInput(attrs={
            'placeholder':'Enter your last name'
        })
    )
    email = forms.EmailField(required=True, validators=[EmailValidator], 
        error_messages={
            'required':'You must enter a email address.'
        },
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter a email address'
        })
    )
    password1 = forms.CharField(max_length=32, required=True, 
        label="Password",
        error_messages={
            'required':'Enter a strong password'
        },
        widget=forms.PasswordInput(attrs={
            'placeholder':"Enter a password"
        }),
        help_text="You password must contain Capital case , numbers and symbols."
    )
    password2 = forms.CharField(max_length=32, required=True,
        label="Password Confirmation",
        error_messages={
            'required':'Enter same password as above'
        },
        widget=forms.PasswordInput(attrs={
                'placeholder':'Enter the same password as above.'
        })
    )

    # Define clean method on a specific field
    # If you use the clean_<field_name> method to raise the validation error, the error is a field error
    # You can access the errors like this in the template {{ form.errors.<field_name> }}
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_('This email is already in use.'), code='unique-email')
        return email

    # Use the clean method to clean fields that depend upon each other. Validation Error raised this way is a non-field-error
    # and can be accessed in the template like so {{ form.non_field_errors }}
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("The two password didn't match."), code="password_mismatch")



class StudentForm(forms.Form):
    YEAR_IN_SCHOOL =[
        ("FR", "Freshman"),
        ("SO", "Sophomore"),
        ("GR", "Graduate"),
        ("JR", "Junior"),
        ("SR", "Senior")
    ]
    name = forms.CharField(max_length=100)
    # You can use the forms.ChoiceField for choice inputs like in the comment below
    # year_in_school = forms.ChoiceField(choices=YEAR_IN_SCHOOL)
    # or you can use form.ChaField and provide the choice in the widget like so:
    year_in_school = forms.CharField(max_length=2, widget=forms.Select(choices=YEAR_IN_SCHOOL))




class UserProfileForm(forms.Form):
    # when you render a form {{ form }} in a template, the default name user to render a form is 'django/forms/default.html',
    # which is a proxy for 'django/forms/table.html'. So a form render in a template will be a table.
    # You can control this by creating an appropriate template and setting a custom FORM_RENDERER to use that template
    # to use site-wide. or 
    # you provide a template_name in the form class like below to use it in a single form like below
    template_name = "Djangoforms/form_snippets.html"
    # Fields which handles relationship
    # This is the example for field which handles relationship
    # In the model UserProfile, the userprofile has ForeignKey relation to the User
    # So this is how you deal with the ForeignKey field in the forms using forms.ModelChoiceField
    # Remember to provide the queryset 
    user = forms.ModelChoiceField(queryset=None,)
    address = forms.CharField(max_length=100)
    date_of_birth = forms.DateField()
    contact_number = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()
        