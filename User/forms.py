from django import forms
from .models import Person,Rationcard
from django.contrib.auth import authenticate,get_user_model

User=get_user_model()

class RationForm(forms.Form):
    username=forms.CharField()
    password=forms.PasswordInput()


    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get['username']
        password=self.cleaned_data.get['password']


        if username and password:
            user=authenticate(RNO=username,password=password)
            
            if not user:
                raise forms.ValidationError("ration id does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("password in incorrect")
        return super(RationForm,self).clean(*args,**kwargs)




    