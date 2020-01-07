
from djongo import models
from django import forms

from django.contrib.auth.models import AbstractUser,User
from django.urls import reverse


class Record(models.Model):
    R_Date=models.DateField(auto_now_add=True)
    R_Quantity=models.FloatField(default=0)
    
        

    class Meta:
        app_label='Distributor'
        






class InputEntry(models.Model):
    I_Date=models.DateField(auto_now=True)
    I_Quantity=models.FloatField()
  
    
        

    class Meta:
        app_label='Distributor'


 

    # add imagefield for GST Receipt

class Stock(models.Model):
    C_ID=models.CharField(max_length=8,primary_key=True)
    C_Name=models.CharField(max_length=20)
    C_Current=models.FloatField(default=0)
    D_Input=models.ArrayModelField(model_container=InputEntry)
    D_Record=models.ArrayModelField(model_container=Record)
    
    def __str__(self):
        return self.C_ID
    
    class Meta:
        app_label='Distributor'


class Inspect(models.Model):
    I_id=models.CharField(max_length=10)
    officer=models.CharField(max_length=100)
    date=models.DateField(auto_now=True)
    file=models.FileField(upload_to='Inspect')
    
    class Meta:
        app_label='Distributor'

class Multicomplain(models.Model):
    complain=models.CharField(max_length=100)

    class  Meta:
        app_label='Distributor'

        
class Complain(models.Model):
    Ration_id=models.CharField(max_length=15)
    Date=models.DateField(auto_now=True)
    status=models.CharField(max_length=20)
    comp=models.ArrayModelField(model_container=Multicomplain)
    
    class Meta:
        app_label='Distributor'




class Distributor(models.Model):
    D_name=models.CharField(max_length=30)
    D_ID=models.CharField(max_length=15,primary_key=True)
    D_Locality=models.CharField(max_length=30)
    D_PIN=models.CharField(max_length=30)
    D_Address=models.CharField(max_length=100)
    D_Stock=models.ArrayModelField(model_container=Stock)
    D_Complain=models.ArrayModelField(model_container=Complain) 
    D_Inspect=models.ArrayModelField(model_container=Inspect)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.D_ID+"  "+self.D_name

    def get_absolute_url(self):
        return reverse('Government:distributormanage')

    class Meta:
        app_label='Distributor'
        



