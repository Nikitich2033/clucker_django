from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from clucker import settings
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    username = models.CharField(
        max_length = 30,
        unique = True,
        validators = [RegexValidator(
            regex=r'^@\w{3,}$',
            message= 'Username must consists of @ symbol followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50,blank = False)
    last_name = models.CharField(max_length=50,blank = False)
    email = models.EmailField(unique= True, blank = False)
    bio = models.CharField(max_length=520, blank = True)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default = 1)
    text = models.CharField(max_length = 280)
    created_at = models.DateTimeField(default = timezone.now)
    class Meta:
        ordering = ["created_at"]
