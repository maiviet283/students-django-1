from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Classes(models.Model):
    name = models.CharField(max_length=5)
    quantity = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(80)]
    )

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.name


class Students(models.Model):
    choices_sex = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    avata = models.ImageField(upload_to='avata/%Y/%m',blank=True,null=True)
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=choices_sex)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=256)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"ID: {self.pk} - Name: {self.name} - Username: {self.username} - {self.age} Years Old"
