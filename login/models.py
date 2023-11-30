from django.db import models

# Create your models here.

class  bloguser(models.Model):
    name= models.CharField(max_length=50)
    email=models.EmailField(max_length=50,primary_key=True,unique=True)
    phone=models.CharField( max_length=50)
    password=models.CharField( max_length=500)

    def __str__(self):
        return f'User :{self.name}'
