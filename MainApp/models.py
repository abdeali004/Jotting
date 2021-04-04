
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class note(models.Model):
    username = models.ForeignKey(
        User, on_delete=models.CASCADE)
    heading = models.TextField()
    main_note = models.TextField(default="")
    datetime_created = models.DateTimeField(auto_now_add=True)


class userInfo(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    email = models.EmailField(max_length=254)
    newUser = models.BooleanField(default=True)
    checkCode = models.CharField(max_length=12)

    def __str__(self):
        return self.username


class verifyUser(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True, max_length=254)
    full_name = models.CharField(max_length=100)
    verificationCode = models.CharField(max_length=12)

    def __str__(self):
        return self.email
