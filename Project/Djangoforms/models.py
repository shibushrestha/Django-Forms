from django.db import models
from django.contrib.auth.models import User

# We are using this model in the formset too.
class Student(models.Model):
    YEAR_IN_SCHOOL =[
        (None, "---------"),
        ("FR", "Freshman"),
        ("SO", "Sophomore"),
        ("GR", "Graduate"),
        ("JR", "Junior"),
        ("SR", "Senior")
    ]
    name = models.CharField(max_length=100,)
    email = models.EmailField(max_length=254)
    year_in_school = models.CharField(max_length=2 , choices=YEAR_IN_SCHOOL)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_number = models.PositiveBigIntegerField()

    def __str__(self):
        return self.user.username
