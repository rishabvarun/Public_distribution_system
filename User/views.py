from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Person,Rationcard,Transact,Quata,systemconfig
from Distributor.models import Distributor,Stock,Record,InputEntry,Complain,Multicomplain,Inspect
from django.http import  HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from .filter import TransactFilter
from Distributor.models import Distributor
# Create your views here.

from django.contrib.auth import authenticate,login,logout
from .models import Person 
from django.db import transaction
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
import random,string 
from Government.fingerprint import give,give1,give3
from django.utils import timezone
from .forms import RationForm
from django.contrib.auth import authenticate,get_user_model,login
from .hardware import give3
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Government.decorators import user_required,distributor_required,admin_required


@login_required
@user_required
def UserWithdrawel(request):
    
    us=request.user.id 
    ration=Rationcard.objects.get(user=us)
    if ration.Category=='APL':
        price=[10,7,0]
    else:
        price=[3,2,13]
    Ration_id=ration.RNO
    ration=Quata.objects.get(ration=Ration_id)
     
    return render(request,'User/withdrawel.html',{'ration':ration,'price':price })
 
@login_required
@user_required
def UserProcessing(request):
    #id=str(random.randint(1,1000000))
    id=''.join(random.choices(string.digits, k = 4)) +''.join(random.choices(string.ascii_uppercase , k =4)) +''.join(random.choices(string.digits, k =4)) 
    Current_Dist=systemconfig.objects.get(id=1)
    D_ID=Current_Dist.D_ID
    us=request.user.id  
    ration=Rationcard.objects.get(user=us)
    R_id=ration.RNO
    
    
    #return HttpResponse(user_id)
    rice=float(request.POST.get('rice',''))
    wheat=float(request.POST.get('wheat',''))
    kerosene=float(request.POST.get('kerosene',''))
    if ration.Category=='APL':
        x=rice*10
        y=wheat*7
        z=kerosene*0
        Total=x+y+z
    else:
        x=rice*3
        y=wheat*2
        z=kerosene*13
        Total=x+y+z
    Dist=Distributor.objects.get(D_ID=D_ID)
    
    ration=Quata.objects.get(ration=R_id)
    if ration.Balance< Total:
       return HttpResponseRedirect("http://127.0.0.1:8000/User/menu/withdrawel/Insufficienfund")
    

    error=[]

 
    with  transaction.atomic():
                  current=Dist.D_Stock[0].C_Current
                  if current<rice:
                      rice=current
                      if rice==0:
                          error.append(['RICE STOCK EXHAUSTED'])
                      else:
                          error.append(['LIMITED RICE STOCK DISPENSING ONLY'+str(rice)+" UNIT"])
                  Dist.D_Stock[0].C_Current-=rice

                  current=Dist.D_Stock[1].C_Current
                  if current<wheat:
                      wheat=current
                      if wheat==0:
                          error.append(['WHEAT STOCK EXHAUSTED'])
                      else :
                          error.append(['LIMITED WHEAT STOCK DISPENSING ONLY'+str(wheat)+" UNIT"])
                  Dist.D_Stock[1].C_Current-=wheat
                  current=Dist.D_Stock[2].C_Current
                  if current<kerosene:
                      kerosene=current
                      if kerosene==0:
                          error.append(['KEROSENE STOCK EXHAUSTED'])
                      else:
                          error.append(['LIMITED KEROSENE STOCK DISPENSING ONLY'+str(kerosene)+" UNIT"])                
                  Dist.D_Stock[2].C_Current-=kerosene
                  Dist.save()

                 
                                
                  ration.Rice_Quata-=rice
                  r_balance=ration.Rice_Quata
                  ration.Wheat_Quata-=wheat
                  w_balance=ration.Wheat_Quata
                  ration.Kerosene_Quata-=kerosene
                  k_balance=ration.Kerosene_Quata
                  ration.Balance-=Total
                  b_balance=ration.Balance
                  Dist.save()
                  ration.save()
                  Transact(Transaction_id=id,Distributor_id=D_ID,Ration_id=R_id,Rice=rice,Wheat=wheat,Kerosene=0,amount=Total).save()
                  
                  subject='test mail'
                  from_email=settings.DEFAULT_FROM_EMAIL
                  a='raikarsiddharth7@gmail.com'
                  to_email=[a]
                  print(timezone.now())

                  context={
                      'user':'siddharth',
                      'useremail':'raikarsiddharth',
                      'rice':rice,
                      'wheat':wheat,
                      'kerosene':kerosene,
                      'Transaction_id':id,
                      'D_ID':D_ID,
                      'R_ID':R_id,
                      'x':x,
                      'y':y,
                      'z':z,
                      'r_balance':r_balance,
                      'w_balance':w_balance,
                      'k_balance':k_balance,
                      'b_balance':b_balance,
                      'Total':Total,
                      'time':str(timezone.now()),
                      'error':error,
        
                    }

                  contact_message=get_template('User/emailtemplate.txt').render(context)
                  send_mail(subject,contact_message,from_email,to_email,fail_silently=True )

    #
    #a=Dist.D_Stock.index(C_ID='123')
    #HttpResponse(a['C_Name'])

    #for stock in Dist.D_Stock:
    logout(request)
    
    return render(request,'User/processing.html',context)

@login_required
@user_required
def insufficient(request):
    logout(request)
    return render(request,'User/insufficientfund.html')




@login_required
@user_required
def UserTransact(request):
    
    return render(request,'User/transactionsucces.html')

class UserFormLogin(forms.Form):
    R_ID = forms.CharField(label=("R_ID"), required=True)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput, required=True)


@login_required

def UserMenu(request):
    #return HttpResponse(give3())
    
    return render(request,'User/menu.html')

@login_required
@user_required
def Userlasttransact(request):
    us=request.user.id
    ration=Rationcard.objects.get(user=us)
    user1=Transact.objects.filter(Ration_id=ration.RNO)
    user1=user1[:10:-1]
    return render(request,'User/last10.html',{'user':user1})


@login_required
@user_required
def UserRationinfo(request):
    us=request.user.id
    ration=Rationcard.objects.get(user=us)
    Ration_id=ration.RNO
    person_list=Person.objects.filter(rationcard=Ration_id)
    return render(request,'User/rationinfo.html',{'person_list':person_list,
                                                'ration':ration, })

class IndexView(ListView):


    model=Transact
    template_name ='User/index1.html'

    

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['filter']=TransactFilter(self.request.GET,queryset=self.get_queryset() )
        return context





class FormLogin(forms.Form):
    D_ID = forms.CharField(label=("D_ID"), required=True)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput, required=True)




# view for the product entry page
class comp1(forms.Form):
    Behave=forms.BooleanField(label='BAD STAFF BEHAVIOUR',required=False)
    stock_quality=forms.BooleanField(label='POOR STOCK QUALITY',required=False)
    stock_quantity=forms.BooleanField(label='INSUFFICIENT STOCK',required=False)
    hygine=forms.BooleanField(label='POOR HYGINE',required=False)
    other=forms.BooleanField(label='OTHER',required=False)



@login_required
@user_required
def AddComplain(request):
   
    us=request.user.id
    ration=Rationcard.objects.get(user=us)
    Ration_id=ration.RNO
    Current_Dist=systemconfig.objects.get(id=1)
    D_ID=Current_Dist.D_ID
    
    Dist=Distributor.objects.get(D_ID=D_ID)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = comp1(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            a=[]
            if form.cleaned_data['Behave']==True:
                a.append(Multicomplain(complain='bad staff behaviour'))
            if form.cleaned_data['stock_quality']==True:
                a.append(Multicomplain(complain='POOR STOCK QUALITY'))
            if form.cleaned_data['stock_quantity']==True:
                a.append(Multicomplain(complain='insufficient stock'))
            if form.cleaned_data['stock_quality']==True:
                a.append(Multicomplain(complain='poor hygine'))
            if form.cleaned_data['other']==True:
                a.append(Multicomplain(complain='other'))
            Dist.D_Complain.append(Complain(Ration_id=Ration_id,Date=timezone.now(),status='Pending'  ,  comp=a))
            Dist.save()

            HttpResponse("http://127.0.0.1:8000/User/login/menu")



    # if a GET (or any other method) we'll create a blank form
    else:
        form = comp1()

    return render(request, 'User/complain.html', {'form': form}) 


def scan_rfid(request):
    username=give3()
 
 

    # create a form instance and populate it with data from the request:
    


    return render(request,'User/scan.html',{'username':username})
  

def login_request(request):       
    username=request.POST.get("username",'')
    password=request.POST.get("password",'')
    print(username)
    print("password")
    print(password)
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        #messages.info(request, f"You are now logged in as {username}")
        return HttpResponseRedirect('http://127.0.0.1:8000/User/menu')
    else:
        return HttpResponseRedirect('http://127.0.0.1:8000/User/incorrect')

    return render(request,'User/logintest.html',)

def home(request):

    return render(request,'User/home.html')

def scancard(request):

    return render(request,'User/scancard.html')

def incorrect(request):

    return render(request,'User/incorrect.html')