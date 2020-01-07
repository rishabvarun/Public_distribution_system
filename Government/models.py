from django.db import models

# Create your models here.



class Circular(models.Model):
    Cid=models.CharField(max_length=10,primary_key=True)
    Cname=models.CharField(max_length=50)
    Cfile=models.FileField(upload_to='cicular')
    Cdate=models.DateField(auto_now=True)


    def __str__(self):
        return self.Cname

