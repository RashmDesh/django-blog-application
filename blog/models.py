from django.db import models
from django.contrib.auth.models import User
from login.models import bloguser



class blogpost(models.Model):
    title = models.CharField(max_length=200)
    auther = models.ForeignKey(to=bloguser,default="",on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField()
    category = models.CharField(max_length=100,default="")
    file = models.FileField(upload_to='static/uploadedfiles',default="")  #where you can upload the file
   
   
    def __str__(self):
        return f'Post title :{self.title}'
