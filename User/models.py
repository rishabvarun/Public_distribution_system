from django.db import models
from django.urls import reverse_lazy
from django.db import transaction
from django.http.response import HttpResponse
from django.http import  HttpResponseRedirect
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser,User
from django import forms
from django.urls import reverse


class Rationcard(models.Model):
    CT=(('APL','APL'),
        ('BPL','BPL'))
    

    RNO=models.CharField(max_length=4,primary_key=True)
    Category=models.CharField(max_length=10,choices=CT,null=True)
    Pin = models.IntegerField()
    Locality_Code=models.IntegerField(default=00000)
    Street=models.CharField(max_length=50)
    H_no=models.CharField(max_length=20)     
    email=models.EmailField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.RNO

    def get_absolute_url(self):
        return reverse('Government:rationmanage')

    
    class Meta:
        app_label='User'

class Quata(models.Model):
    

    Rice_Quata=models.FloatField()
    Wheat_Quata=models.FloatField()
    Kerosene_Quata=models.FloatField()
    Balance=models.IntegerField(default=0)
       
    ration=models.ForeignKey(Rationcard,on_delete=models.CASCADE)



        
class Transact(models.Model):
    Transaction_id = models.CharField(max_length=12)
    Distributor_id=models.CharField(max_length=12)
    Ration_id=models.CharField(max_length=12) 
    Rice=models.FloatField(default=0)
    Wheat=models.FloatField(default=0)
    Kerosene=models.FloatField(default=0)
    Date=models.DateField(auto_now=True,)
    amount=models.FloatField()
    time=models.TimeField(auto_now=True)






    class Meta:
        app_label='User'



class Person(models.Model):
    Fname=models.CharField(max_length=50,null=True)
    Mname=models.CharField(max_length=50,null=True)
    Lname=models.CharField(max_length=50,null=True)
    aadhar=models.CharField(max_length=16,unique=True)
    DOB=models.DateField(null=True)
    age=models.IntegerField()
    sex=models.CharField(max_length=10)
    fingerprint=models.IntegerField()
    photo=models.ImageField(upload_to='person_image')
    rationcard=models.ForeignKey(Rationcard,on_delete=models.CASCADE)


    def __str__(self):
        return self.Fname+" "+self.Mname+" "+self.Lname

    def get_absolute_url(self):
        return reverse('Government:rationmanage')

    

  
        

    class Meta:
        app_label='User'




class systemconfig(models.Model):
    D_name=models.CharField(max_length=50)
    D_ID=models.CharField(max_length=15)










 