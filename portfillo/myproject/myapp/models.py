from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class signup_page(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100, validators=[MinLengthValidator(6)])
    confirm_password = models.CharField(max_length=100, validators=[MinLengthValidator(6)])
    
class message_sending(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()