from django.shortcuts import render, redirect
from .forms import UserRegisterForm, StudentForm, UserProfileForm

from django.contrib.auth.models import User
from .models import Student, UserProfile

def home(request):
    return render(request, 'Djangoforms/home.html')


def register_user(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
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
    form = StudentForm()
    # For singlerender of form instance you can pass template_name to the Form.render() method
    rendered_form = form.render("Djangoforms/form_snippets.html")
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            year_in_school = form.cleaned_data.get('year_in_school')

            student = Student.objects.create(name=name, year_in_school=year_in_school)
            return redirect('/Djangoforms/')
    return render(request, 'Djangoforms/student-register.html', {'form':rendered_form})



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