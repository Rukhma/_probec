from django.db import models

# Create your models here.
class Userreg(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    class Meta:
        db_table='users'
        app_label='signup.models.Userreg'