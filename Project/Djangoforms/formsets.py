# FORMSETS
# A formset is a layer of abstraction to work with multiple forms on the same page. It can be best compared to a data grid

# formset_factory(form, formset=BaseFormSet, extra=1, can_order=False, can_delete=False, max_num=None, validate_max=
# False, min_num=None, validate_min=False, absolute_max=None, can_delete_extra=True, renderer=None)


from django.forms import formset_factory
from .forms import StudentForm

StudentFormset = formset_factory(StudentForm, extra=9, max_num=100, validate_max=True, min_num=1, validate_min=True)