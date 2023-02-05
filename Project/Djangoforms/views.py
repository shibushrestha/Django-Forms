from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Student, UserProfile
from .forms import UserRegisterForm, StudentForm, UserProfileForm
from .modelforms import UserRegistrationForm
from .formsets import StudentFormset, StudentFormset1

def home(request):
    return render(request, 'Djangoforms/home.html')


def register_user(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST,)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password2 = form.cleaned_data.get('password2')

            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password2)
            user.save()

            return redirect('/Djangoforms/')
            
    return render(request, 'Djangoforms/register.html', {'form':form})


def student_register(request):
    form = StudentForm(initial={'name':'Shibu Shrestha', 'year_in_school':'FR'})
    # For single render of form instance you can pass template_name to the Form.render() method
    # rendered_form = form.render("Djangoforms/form_snippets.html",)
    print(form.is_valid())
    if request.method == "POST":
        form = StudentForm(request.POST,)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('/Djangoforms/')
    return render(request, 'Djangoforms/student-register.html', {'form': form})



def userprofile(request):
    # Initial value is being used as fallback value and I don't know why?
    form = UserProfileForm(initial={'address':"Samakhushi"})
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            address = form.cleaned_data.get('address')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            contact_number = form.cleaned_data.get('contact_number')
            userprofile = UserProfile.objects.create(
                user =user,
                address = address,
                date_of_birth = date_of_birth,
                contact_number = contact_number
            )

            return redirect("/Djangoforms/")

    return render(request, 'Djangoforms/userprofile.html', {'form':form})



# This view uses the ModelForm from modelforms.py

def user_registration(request):
    user = request.user
    form = UserRegistrationForm(instance=user)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/Djangoforms/")
    return render(request, 'Djangoforms/user_registration.html', {'form':form})


# This view is for the StudentFormset
def add_students(request):
    student_formset = StudentFormset1(prefix='student',)
    if request.method == 'POST':
        student_formset = StudentFormset1(request.POST, prefix='student', error_messages={'too_few_forms': 'You must at least submit one form.'})
        if student_formset.is_valid():
            for form in student_formset.forms:
                if form.has_changed():
                    if form.is_valid():
                        form.save()
                    else:
                        return render(request, 'Djangoforms/add_students.html', {'student_formset':student_formset})
            return redirect('/Djangoforms/')
    return render(request, 'Djangoforms/add_students.html', {'student_formset':student_formset})