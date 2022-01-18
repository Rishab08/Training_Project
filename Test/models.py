from django.db import models


class Test(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)



    def __str__(self):
        return self.username
