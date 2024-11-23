from django.db import models

class Parent(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    age=models.IntegerField(default=1)

# Create your models here.
class Children(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    age=models.IntegerField(default=1)
    parent=models.ForeignKey(Parent,on_delete=models.CASCADE,null=True)
