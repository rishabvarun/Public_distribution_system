import django_filters
from .models import Transact,Person,Rationcard
from Government.models import Circular
from Distributor.models import Distributor



class UserFilter(django_filters.FilterSet):
    #Ration_id = django_filters.CharFilter(lookup_expr='icontains')
    #year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    #year_joined__gt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__gt')
    #year_joined__lt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__lt')
    class Meta:
        model = Transact
        #fields = ['Ration_id', 'Date', ]
        fields = {
            'Ration_id': ['icontains', ],
           
            'Date': ['range' ],
         }



class  CircularFilter(django_filters.FilterSet):

    class Meta:
        model=Circular
        fields={
              'Cid':['icontains'],
               'Cname':['icontains'],
               'Cdate':['lte']}


class  DistributorFilter(django_filters.FilterSet):

    class Meta:
        model=Distributor
        fields={
              'D_ID':['icontains'],
               'D_name':['icontains'],
              'D_PIN':['icontains'],
              'D_Locality':['icontains'],
              }

class  PersonFilter(django_filters.FilterSet):

    class Meta:
        model=Person
        fields={
              'Fname':['icontains'],
               'Lname':['icontains'],
              'aadhar':['exact'],
              'rationcard':['exact'],
              }

class  RationFilter(django_filters.FilterSet):

    class Meta:
        model=Rationcard
        fields={
              'RNO':['icontains'],
               'Locality_Code':['icontains'],
              'Pin':['icontains']
              }

class  TransactFilter(django_filters.FilterSet):

    class Meta:
        model=Transact
        fields={
              'Transaction_id':['icontains'],
               'Distributor_id':['icontains'],
              'Ration_id':['icontains'],
              'Date':['exact'],
              }