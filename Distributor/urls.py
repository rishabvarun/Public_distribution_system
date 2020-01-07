from django.urls import  path
from .import views
from Government.views import DistributorSignUpView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from User.filter import CircularFilter,DistributorFilter,PersonFilter
from django_filters.views import FilterView

app_name = 'Distributor'

urlpatterns = [
    path('login/home/logout',views.logout1),
    
    path('',views.systemconfig1),
    path('success',views.systemsuccess),
    path('fail',views.systemfail),
    path('home',views.home,name='home'),
    path('home/stock',views.StockDetail),
    path('home/recordentry',views.RecordData),
    path('home/inputentry',views.InputData),
    path('home/update',views.UpdateRecord),
    path('home/complain',views.complainview),
    path('home/inspect',views.Inspectview),
    # path('entry',views.AddEntry),
    path('home/addinput',views.AddInputEntry),
     path('home/addinput/succes',views.inputsucces),
      path('home/circularview', FilterView.as_view(filterset_class=CircularFilter,
        template_name='Distributor/circular_list.html'), name='search'),
      
    
  

]

urlpatterns += staticfiles_urlpatterns()
