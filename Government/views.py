from django.shortcuts import render,redirect
from User.models import Person,systemconfig
from django.shortcuts import render
from django.http.response import HttpResponse
from django.utils import timezone
from django.http import  HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.generic import ListView
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from .models import Circular
from Distributor.models import Distributor,Stock,Record,InputEntry,Complain,Multicomplain,Inspect
from django.contrib.auth.models import User
# Create your views here.
from User.models import Rationcard,Person,Quata
from django.db import transaction
from django import forms

from django.conf import settings
from .forms import PersonForm1
from django.core.mail import send_mail
from django.template.loader import get_template
import random,string 
from User.filter import CircularFilter
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth import login,logout
import json
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.csrf import csrf_exempt 
from . import checksum as Checksum
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import user_required,distributor_required,admin_required
# Create your views here

MERCHANT_KEY = 'JcZhIlup0QOe5tzW'

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        
   
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Balance successful added')
            RNO=response_dict['ORDERID'][-4:len(response_dict['ORDERID'])]
            Qt=Quata.objects.get(ration=RNO)
            Qt.Balance+=int(float((response_dict['TXNAMOUNT'])))
            Qt.save()

        else:
            print('Balance  was not successful added because' + response_dict['RESPMSG'])
    return render(request, 'Government/paymentstatus.html', {'response': response_dict})



@login_required
@admin_required
def AddBalance(request,RNO):
  
    form=BalanceForm()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
                # create a form instance and populate it with data from the request:
        form = BalanceForm(request.POST,request.FILES)
        amount=request.POST.get('amount','')

        id=''.join(random.choices(string.digits, k = 4)) +''.join(random.choices(string.ascii_uppercase , k =4)) +''.join(random.choices(string.digits, k =4))+''.join(RNO)
        
            # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'nvmbbA22073778596899',
                'ORDER_ID': id,
                'TXN_AMOUNT': amount,
                'CUST_ID': RNO,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/Government/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'Government/paytm.html', {'param_dict': param_dict})



    return render(request, 'Government/balance.html', {'form': form}) 

@login_required
@admin_required
def GovernmentRationinfo(request,RNO):
    
    ration=Rationcard.objects.get(RNO=RNO)
    person_list=Person.objects.filter(rationcard=RNO)
    return render(request,'Government/rationinfo.html',{'person_list':person_list,
                                                'ration':ration, })



class DateInput(forms.DateInput):
    input_type='date'


class PersonForm(forms.ModelForm):
    
    DOB=forms.DateField(widget=DateInput)
    class Meta:
        model=Person
        fields='__all__'

class DistributorForm(forms.ModelForm):
    
    
    class Meta:
        model=Distributor
        fields=['D_name','D_ID','D_Address','D_PIN','D_Locality']

class CreateDistributor1(UserCreationForm):
    D_name=forms.CharField(max_length=50)
    D_ID=forms.CharField(max_length=50)
    D_Address=forms.CharField(max_length=50)
    D_PIN=forms.CharField(max_length=50)
    D_Locality=forms.CharField(max_length=50)




    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                        Row(
                Column('username', css_class='form-group col-md-6 mb-0'),                
                css_class='form-row'
            ),
            'password1',
            'password2',
       
            Row(
                Column('D_name', css_class='form-group col-md-4 mb-0'),
                Column('D_ID', css_class='form-group col-md-4 mb-0'),
               
                css_class='form-row'
            ),
            
          
            
                Row(
                Column('D_Address', css_class='form-group  col-md-4 mb-0'),
                 Column('D_Locality', css_class='form-group col-md-4 mb-0'),
                Column('D_PIN', css_class='form-group  col-md-4 mb-0'),
                css_class='form-row'
            ),
                 

               

            Submit('submit', 'Register')
        )


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name ='distributor'
        user.save()
        dist=Distributor.objects.create(user=user,
        D_name=self.cleaned_data['D_name'],
        D_ID=self.cleaned_data['D_ID'],
        D_Address=self.cleaned_data['D_Address'],
        D_PIN=self.cleaned_data['D_PIN'],
        D_Locality=self.cleaned_data['D_Locality'],
        D_Stock=[],
        D_Complain=[],
        D_Inspect=[])
        dist.save()
        return user

@method_decorator([login_required, admin_required], name='dispatch')
class DistributorSignUpView(generic.CreateView):
    
    model = User
    form_class = CreateDistributor1
    template_name = 'registration/signup.html'



    def form_valid(self, form):
        D_ID=form.cleaned_data['D_ID']
        user = form.save()
        login(self.request, user)
        return redirect('Government:appendstock',D_ID)

class Createration1(UserCreationForm):
    
    RNO=forms.CharField(max_length=50)
    Category=forms.CharField(widget=forms.Select(choices=Rationcard.CT))
    Pin=forms.CharField(max_length=50)
    Locality=forms.IntegerField()
    Street=forms.CharField(max_length=50)
    H_no=forms.CharField(max_length=20)     
    email=forms.EmailField()
    




    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                        Row(
                Column('username', css_class='form-group col-md-6 mb-0'),                
                css_class='form-row'
            ),
            'password1',
            'password2',
       
            Row(
                Column('RNO', css_class='form-group col-md-4 '),
               Column('Category', css_class='form-group col-md-4 '),
                css_class='form-row'
            ),

                           Row(
                Column('H_no', css_class='form-group col-md-4 mb-0'),
                Column('Street', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
            
            Row(
                Column('Locality', css_class='form-group col-md-4 mb-0'),
                
                Column('Pin', css_class='form-group col-md-4 mb-0'),
              
                css_class='form-row'
            ),
            
         
                       

             
                          Row(
                Column('email', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
                     




            Submit('submit', 'Register')
        )


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = 'ration'
        user.save()
        ration=Rationcard.objects.create(user=user,
        RNO=self.cleaned_data['RNO'],
        Category=self.cleaned_data['Category'],
        Pin=self.cleaned_data['Pin'],
        Locality_Code=self.cleaned_data['Locality'],
        Street=self.cleaned_data['Street'],
        H_no=self.cleaned_data['H_no'],
        email=self.cleaned_data['email'],        
        )

        ration.save()
        Quata(Rice_Quata=10,Wheat_Quata=10,Kerosene_Quata=10,Balance=100,ration=ration).save()
        return user

@method_decorator([login_required, admin_required], name='dispatch')
class RationSignUpView(generic.CreateView):
    
    model = User
    form_class = Createration1
    template_name = 'registration/signup.html'



    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect("http://127.0.0.1:8000/Government/login/home")



class StockForm(forms.Form):
    rice=forms.IntegerField()
    wheat=forms.IntegerField()
    kerosene=forms.IntegerField()

@login_required
@admin_required
def AppendStock(request,D_ID):
    # if this is a POST request we need to process the form data
   
    #del(request.session['D_ID'])
    Dist=Distributor.objects.get(D_ID=D_ID)
    
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form =StockForm(request.POST,request.FILES)
       
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            
           
            Dist.D_Stock.append(Stock(C_Name='Rice',
                                    C_ID='123'
                                    ,C_Current=form.cleaned_data['rice'] ,
                                    D_Input=[InputEntry(I_Quantity=form.cleaned_data['rice'],I_Date=timezone.now())] , 
                                    D_Record=[]
                                    )
                                    )
            Dist.D_Stock.append(Stock(C_Name='Wheat',
                                    C_ID='856'
                                    ,C_Current=form.cleaned_data['wheat'] ,
                                    D_Input=[InputEntry(I_Quantity=form.cleaned_data['wheat'],I_Date=timezone.now())]  , 
                                    D_Record=[]
                                    )
                                    )
            Dist.D_Stock.append(Stock(C_Name='Kerosene',
                                    C_ID='675'
                                    ,C_Current=form.cleaned_data['kerosene'],
                                    D_Input=[InputEntry(I_Quantity=form.cleaned_data['kerosene'],I_Date=timezone.now())] , 
                                    D_Record=[]
                                    )
                                    )
            Dist.save()




            
            return HttpResponseRedirect('http://127.0.0.1:8000/Government/login/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StockForm()

                                             
     

        
    return render(request, 'Government/stockform.html', {'form': form})    







class CircularForm(forms.ModelForm):


    class Meta:
        model=Circular
        fields='__all__'

@login_required
@admin_required
def AddCircular(request):


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form =CircularForm(request.POST,request.FILES)
        print("test")
        # check whether it's valid:
        if form.is_valid():
           print("test")
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a
            #  new URL:
           form.save()     
           
                        
           return HttpResponseRedirect('http://127.0.0.1:8000/Government/login/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CircularForm()

    return render(request, 'Government/circularform.html', {'form': form}) 

@login_required
@admin_required
def Circularview(request):
    circular=Circular.objects.all()


    return render(request,'Government/circular_list.html',{'circular':circular})


@method_decorator([login_required, admin_required], name='dispatch')
class CircularIndexView(ListView):


    model=Circular
    template_name ='Government/cicular_list.html'

    

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['filter']=CircularFilter(self.request.GET,queryset=self.get_queryset() )
        return context






@login_required
@admin_required
def CreatePerson(request,RNO):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PersonForm1(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():

            fn=form.cleaned_data['First_name']
            mn=form.cleaned_data['Middle_name']
            ln=form.cleaned_data['Last_name']
            aadhar=form.cleaned_data['aadhar']
            finger=form.cleaned_data['finger']
            sex=form.cleaned_data['sex']
            age=form.cleaned_data['age']
            DOB=form.cleaned_data['DOB']
            photo=form.cleaned_data['photo']
            ration=Rationcard.objects.get(RNO=RNO)
            Person(Fname=fn,Mname=mn,Lname=ln,aadhar=aadhar,DOB=DOB,sex=sex,
                   fingerprint=finger,rationcard=ration,photo=photo,age=age).save()
            
            return HttpResponseRedirect('http://127.0.0.1:8000/Government/login/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PersonForm1()

    return render(request, 'Government/personform1.html', {'form': form}) 





class InspectForm(forms.ModelForm):

    class Meta:
        model=Inspect
        fields={'I_id','officer','file'}

@login_required
@admin_required
def AddInspect(request,D_ID):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InspectForm(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            Dist=Distributor.objects.get(D_ID=D_ID)
          


            Dist.D_Inspect.append(Inspect(I_id=form.cleaned_data['I_id'],
                                officer=form.cleaned_data['officer'],
                        date=timezone.now(),
                        file=form.cleaned_data['file']))
            Dist.save()

            return HttpResponseRedirect('http://127.0.0.1:8000/Government/login/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InspectForm()

    return render(request, 'Government/inspect.html', {'form': form})     








def home1(request):

    return render(request,'Government/home.html',)

@login_required
@admin_required
def refilration(request):
    rationcd=Rationcard.objects.all()
    
    
    
    with transaction.atomic():
        for x in rationcd:
            ration_Q=Quata.objects.get(ration=x.RNO)
            print(ration_Q.ration)
            if x.Category=='APL':
                ration_Q.Rice_Quata=7
                ration_Q.Wheat_Quatat=15
                ration_Q.Kerosene_Quata=0
            else:
                ration_Q.Rice_Quata=15
                ration_Q.Wheat_Quata=20
                person=Person.objects.filter(rationcard=x.RNO)
                num=len(person)
                ration_Q.Kerosene_Quata=num

          
            ration_Q.save()
    return render(request,'Government/renew.html')

class BalanceForm(forms.Form):
    
    amount=forms.IntegerField(min_value=0)


  

@login_required
@admin_required
def Inspectview(request,D_ID):
    
    Dist=Distributor.objects.get(D_ID=D_ID)
    return render(request,'Government/inspectview.html',{'Dist':Dist})


@login_required
@admin_required
def Complainview(request,D_ID):
    Dist=Distributor.objects.get(D_ID=D_ID)
    
    return render(request,'Government/complainview.html',{'Dist':Dist})



@login_required
@admin_required
def CreateQuata(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuataForm(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            form.save()

            #Quata(Rice_Quata=10,Wheat_Quata=10,Kerosene_Quata=10,Balance=100,ration=rno).save()
            return HttpResponseRedirect('http://127.0.0.1:8000/Government/login/home')
    else:
        form = RationForm()

    return render(request, 'Government/person_form.html', {'form': form})


@login_required
@admin_required
def logout2(request):
    logout(request)

    return render(request,'Government/logout.html')

@login_required
@admin_required
def home(request):
    return render(request,'Government/home2.html')
    return render(request,'Government/home2.html')

@login_required
@admin_required
def StockDetail(request,D_ID):
    Dist_info=Distributor.objects.get(D_ID=D_ID)
    return render(request,'Government/stockinfo.html',{'Dist_info':Dist_info}
                                                      )

@login_required
@admin_required
def InputData(request,D_ID):
   
    stock_name=request.POST.get('stock_name','')
    Dist_info=Distributor.objects.get(D_ID=D_ID)
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
    return render(request,'Government/inputview.html',{'Dist_info':Dist_info,'stock_name':stock_name,'send':send,'json_list': json_list})

@login_required
@admin_required
def RecordData(request,D_ID):
    #D_key=request.session['D_key']
    stock_name=request.POST.get('stock_name','')
    print(stock_name)
    us=request.user.id
    Dist_info=Distributor.objects.get(D_ID=D_ID)
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
    return render(request,'Government/recordview.html',{'Dist_info':Dist_info,'stock_name':stock_name,'send':send,'json_list': json_list})


def test(request):


    return render(request,'Government/gridtest.html')

from django.views.generic.edit import UpdateView


@method_decorator([login_required, admin_required], name='dispatch')
class PersonUpdate(UpdateView):
    model = Person
    fields = '__all__'
    template_name= 'Government/person_form.html'

@method_decorator([login_required, admin_required], name='dispatch')
class PersonDelete(DeleteView):
    model = Person
    template_name= 'Government/delete.html'
    success_url = reverse_lazy('Government:rationmanage')



@method_decorator([login_required, admin_required], name='dispatch')
class RationUpdate(UpdateView):
    model = Rationcard
    fields = ['RNO','H_no','Street','Locality_Code','Pin','email','Category']
    template_name= 'Government/Rationform.html'

@method_decorator([login_required, admin_required], name='dispatch')
class RationDelete(DeleteView):
    model = Rationcard
    template_name= 'Government/delete.html'
    success_url = reverse_lazy('Government:rationmanage')


@method_decorator([login_required, admin_required], name='dispatch')
class DistributorUpdate(UpdateView):
    model = Distributor
    fields = ['D_name','D_ID','D_Address','D_Locality','D_PIN']
    template_name= 'Government/Distributorform.html'

@method_decorator([login_required, admin_required], name='dispatch')
class DistributorDelete(DeleteView):
    model = Distributor
    template_name= 'Government/delete.html'
    success_url = reverse_lazy('Government:distributormanage')