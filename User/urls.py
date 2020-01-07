from django.urls import  path
from .import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django import forms
from django_filters.views import FilterView
from .filter import UserFilter
app_name = 'User'



urlpatterns = [
   
     path('',views.home),
     path('scancard',views.scancard),
     path('incorrect',views.incorrect),
    path('menu',views.UserMenu),
    path('menu/withdrawel',views.UserWithdrawel),
    path('menu/withdrawel/processing',views.UserProcessing),
    path('menu/withdrawel/processing/success',views.UserTransact),
    path('menu/rationinfo',views.UserRationinfo),
    path('menu/lasttranaction',views.Userlasttransact),
    path('menu/complain',views.AddComplain),
    path("menu/withdrawel/Insufficienfund",views.insufficient),
   # path('pdftest',views.pdf_view),
    #path('pdftest',views.pdf_view),
    #path('pdftest',views.pdf_view),
      url('search', FilterView.as_view(filterset_class=UserFilter,
        template_name='User/filtering.html'), name='search'),

      path("scan",views.scan_rfid),
      path('scan/login',views.login_request),
 # path('config',views.session_demo),
 # path('processing',views.processing),
 # modelforms/person/entry
   
]

urlpatterns += staticfiles_urlpatterns()
