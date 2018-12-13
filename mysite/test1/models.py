from django.db import models


class UserManager(models.Manager):
    pass

class User(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    name=models.CharField(max_length=20,)
    gender=models.CharField(max_length=5,)
    age = models.IntegerField(max_length=5,)

    # user_manager=UserManager()