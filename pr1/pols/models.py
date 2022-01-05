from django.db import models

# Create your models here.
class Student(models.Model):
                 s_id=models.AutoField
                 s_name=models.CharField(max_length=50)
                 course=models.CharField(max_length=50)
                 adm_date=models.DateField()
