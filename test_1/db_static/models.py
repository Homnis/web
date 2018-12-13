from django.db import models

# Create your models here.
class User(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    name=models.CharField(max_length=20,unique=True)
    psw=models.CharField(max_length=20,)
    gender=models.CharField(max_length=5,)
    age = models.IntegerField()
    address=models.CharField(max_length=255,null=True)

