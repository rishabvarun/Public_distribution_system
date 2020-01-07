from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView
from Distributor.models import Distributor
from django.urls import reverse_lazy
from django import forms
from django.views.generic import ListView
from django.http.response import HttpResponse,HttpResponseRedirect
from .models import Distributor,Stock,Record,InputEntry,Complain,Multicomplain,Inspect
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Government.decorators import user_required,distributor_required,admin_required

from User.models import systemconfig

import json

class ConfigarationForm(forms.Form):
    username=forms.CharField(max_length=60,required=True)
    password=forms.CharField(label=("Password"), widget=forms.PasswordInput, required=True)





def systemconfig1(request):


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form =ConfigarationForm(request.POST)

        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is None:
                return HttpResponseRedirect("http://127.0.0.1:8000/Distributor/fail")
            if user.first_name=='distributor':
                us=user.id
                Dist=Distributor.objects.get(user=us)
                Current_Dist=systemconfig.objects.get(id=1)
                Current_Dist.D_name=Dist.D_name
                Current_Dist.D_ID=Dist.D_ID
                Current_Dist.save()

             

                return HttpResponseRedirect("http://127.0.0.1:8000/Distributor/success")
            else:
                return HttpResponseRedirect("http://127.0.0.1:8000/Distributor/fail")

                  
           
                        
           


    else:
        form = ConfigarationForm()

    return render(request, 'Distributor/systemconfigaration.html', {'form': form}) 

def systemsuccess(request):
    return render(request,'Distributor/systemsuccess.html')

def systemfail(request):
    return render(request,'Distributor/systemfail.html')



@login_required
@distributor_required
def home(request):
    #Dist=Distributor.objects.all()
    us=request.user.id
    Dist_info=Distributor.objects.get(user=us)

    return render(request,'Distributor/home.html',{'Dist_info':Dist_info})

 



@login_required
@distributor_required
def StockDetail(request):
    #D_key=request.session['D_key']
    us=request.user.id
    Dist_info=Distributor.objects.get(user=us)
    

    return render(request,'Distributor/stockinfo.html',{'Dist_info':Dist_info})

@login_required
@distributor_required
def InputData(request):
   
    stock_name=request.POST.get('stock_name','')
    us=request.user.id
    Dist_info=Distributor.objects.get(user=us)
    if(stock_name=='Rice'):
        send=Dist_info.D_Stock[0].D_Input
    elif(stock_name=='Wheat'):
        send=Dist_info.D_Stock[1].D_Input
    else:
        send=Dist_info.D_Stock[2].D_Input
    
    big=[]
    big.append(['Date','Quantity'])
    print(stock_name)
    for x in send:
        big.append([str(x.I_Date),x.I_Quantity])
   
    
    json_list = json.dumps(big)
    

    
    #return HttpResponse(stock_name)
    return render(request,'Distributor/inputview.html',{'Dist_info':Dist_info,'stock_name':stock_name,'send':send,'json_list': json_list})

@login_required
@distributor_required
def RecordData(request):
    #D_key=request.session['D_key']
    stock_name=request.POST.get('stock_name','')
    print(stock_name)
    us=request.user.id
    Dist_info=Distributor.objects.get(user=us)
    if(stock_name=='Rice'):
        send=Dist_info.D_Stock[0].D_Record
    elif(stock_name=='Wheat'):
        send=Dist_info.D_Stock[1].D_Record
    else:
        send=Dist_info.D_Stock[2].D_Record
    
    big=[]
    big.append(['Date','Quantity'])
    
    for x in send:
        big.append([str(x.R_Date),x.R_Quantity])
   
    
    json_list = json.dumps(big)
    
    
    
    return render(request,'Distributor/recordview.html',{'Dist_info':Dist_info,'stock_name':stock_name,'send':send,'json_list': json_list})



        #fields=['C_ID','C_Name','I_Date','I_Quantity','I_Gst']
@login_required
@distributor_required
def UpdateRecord(request):

    us=request.user.id
    Dist=Distributor.objects.get(user=us)
 
    for stock in Dist.D_Stock:
        stock.D_Record.append(Record(R_Quantity=stock.C_Current,R_Date=timezone.now()))
    Dist.save()
    #Dist.D_Stock[1].D_Record.append(Record(R_Quantity=Dist.D_Stock[1].C_Current,R_Date=timezone.now()))
    

    
    return render(request, 'Distributor/record_entry.html', {})



class InputForm(forms.ModelForm):

    class Meta:
        model=InputEntry 
        fields='__all__'



@login_required
@distributor_required
def AddInputEntry(request):
    # if this is a POST request we need to process the form data
    us=request.user.id
    Dist=Distributor.objects.get(user=us)

    if request.method == 'POST':
       if request.POST.get('rc',''):
           Dist.D_Stock[0].D_Input.append(InputEntry(I_Date=timezone.now(),I_Quantity=request.POST.get("rice",'')))
           Dist.D_Stock[0].C_Current+=float(request.POST.get("rice",''))

       if request.POST.get('wc',''):
           Dist.D_Stock[1].D_Input.append(InputEntry(I_Date=timezone.now(),I_Quantity=request.POST.get("wheat",'')))
           Dist.D_Stock[1].C_Current+=float(request.POST.get("wheat",''))

       if request.POST.get('kc',''):
           Dist.D_Stock[2].D_Input.append(InputEntry(I_Date=timezone.now(),I_Quantity=request.POST.get("kerosene",'')))                                         
           Dist.D_Stock[2].C_Current+=float(request.POST.get("kerosene",''))

       Dist.save()
       return HttpResponseRedirect("http://127.0.0.1:8000/Distributor/home/addinput/succes")

          
            


   

    return render(request,'Distributor/addinput.html', )    

def logout1(request):
    logout(request)

    return render(request,'Distributor/logout.html')


def inputsucces(request):


    return render(request,"Distributor/inputsucces.html",)

@login_required
@distributor_required
def complainview(request):
    us=request.user.id
    Dist=Distributor.objects.get(user=us)
    return render(request,'Distributor/complainview.html',{'Dist':Dist})

@login_required
@distributor_required
def Inspectview(request):
    us=request.user.id
    Dist=Distributor.objects.get(user=us)
     
    return render(request,'Distributor/inspectview.html',{'Dist':Dist})