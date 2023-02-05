# FORMSETS
# A formset is a layer of abstraction to work with multiple forms on the same page. It can be best compared to a data grid

# formset_factory(form, formset=BaseFormSet, extra=1, can_order=False, can_delete=False, max_num=None, validate_max=
# False, min_num=None, validate_min=False, absolute_max=None, can_delete_extra=True, renderer=None)


from django.forms import formset_factory
from .forms import StudentForm

StudentFormset = formset_factory(StudentForm, extra=10, max_num=10, validate_max=True, min_num=1, validate_min=True, can_delete=True)



# ERROR_MESSAGES
# These are errors related to the formset and not the forms, you can access these error by formset.non_form_errors
# too_few_forms
# too_many_forms
# missing_management_form

# You can override the above messages in the formset like this:

# formset = StudentFormset(error_messages={'too_few_forms' : 'You must atleast submit five forms' })



# ADDING ADDITIONAL FIELDS TO THE FORMSET
# BaseFormSet provides a 'add_fields' method which you can override to add additional fields to the formset

from django.forms import BaseFormSet
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class BaseStudentFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['email'] = forms.EmailField(required=True, error_messages={'required':'You must provide a email address'})


    'Check that no student has the same email address'
    def clean(self):
        " Don't bother validating the formset unless each form is valid on its own. "
        if any(self.errors):
            return
        emails=[]
        for form in self.forms:
            # We are checking if the forms in the formset has changed or not, and only comparing the emails of those changed form
            # If we don't do this form.cleaned_data.get('email') will return emails from the empty forms and throw the error
            # because they are all empty and same.
            if form.has_changed():
                email = form.cleaned_data.get('email')
                if email in emails:
                    raise ValidationError(_('Students cannot have the same email address.'), code="same_email")
                emails.append(email)


StudentFormset1 = formset_factory(StudentForm, formset=BaseStudentFormSet, extra=10, max_num=10, validate_max=True, min_num=1, validate_min=True, can_delete=True)
