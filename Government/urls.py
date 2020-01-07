from django.urls import  path
from .import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django_filters.views import FilterView
from User.filter import CircularFilter,DistributorFilter,PersonFilter,TransactFilter,RationFilter
from .views import DistributorSignUpView,RationSignUpView

app_name = 'Government'

urlpatterns = [

    path("login/home",views.home1),
    path("login/home/logout",views.logout2),
    path('login/home/ration',RationSignUpView.as_view()),
     path('login/home/createdistributor',DistributorSignUpView.as_view()),
    path('login/home/createperson',views.CreatePerson),
   
    
    path('login/home/appendstock/<str:D_ID>/',views.AppendStock,name='appendstock'),
    path('login/home/addinspect/<str:D_ID>/',views.AddInspect,name='addinspection'),
    path('login/home/addcircular',views.AddCircular),
  
    path('login/home/Distributorsearch', FilterView.as_view(filterset_class=DistributorFilter,
        template_name='Government/distributorsearch.html'), name='search'),
    path('login/home/Personsearch', FilterView.as_view(filterset_class=PersonFilter,
        template_name='Government/persondetail.html'), name='Personsearch'),
    #path('circularview',views.Circularview),
    path('login/home/circularview', FilterView.as_view(filterset_class=CircularFilter,
        template_name='Government/circular_list.html'), name='search'),
    path('login/home/transactionview', FilterView.as_view(filterset_class=TransactFilter,
        template_name='Government/transactionview.html'), name='search'),
    path('login/home/rationview', FilterView.as_view(filterset_class=RationFilter,
        template_name='Government/rationcardfilter.html'), name='search'),

    path('login/home/addbalance/<str:RNO>/',views.AddBalance ,name='addbalance'),

    path('login/home/Distributormanage/inspectview/<int:D_ID>/',views.Inspectview,name='inspectionview'),
    path('login/home/Distributormanage/complainview/<int:D_ID>/',views.Complainview ,name='complainview'),
   

  
    path('login/home/renew',views.refilration),
  
  
     path('login/home/stockdetail/<str:D_ID>/',views.StockDetail,name='stockdetail'),
     path('login/home/stockdetail/<str:D_ID>/inputentry',views.InputData,name='inputentry'),
     path('login/home/stockdetail/<str:D_ID>/recordentry',views.RecordData,name='recordentry'),
         path('login/home/Distributormanage', FilterView.as_view(filterset_class=DistributorFilter,
        template_name='Government/distributormanage.html'), name='distributormanage'),
           path('login/home/Rationmanage', FilterView.as_view(filterset_class=RationFilter,
        template_name='Government/rationmanage.html'), name='rationmanage'),
           path('login/home/Rationmember/<str:RNO>/',views.GovernmentRationinfo,name='rationinfo'),
            path("login/home/createperson/<str:RNO>",views.CreatePerson,name='createperson'),

      path('test',views.test),


      path("handlerequest/",views.handlerequest,name='Handlerequest'),



      url(r'^person/(?P<pk>[0-9]+)/$', views.PersonUpdate.as_view(), name='person-update'),
       url(r'^person/(?P<pk>[0-9]+)/delete$', views.PersonDelete.as_view(), name='person-delete'),

      url(r'^ration/(?P<pk>[0-9]+)/$', views.RationUpdate.as_view(), name='ration-update'),
         url(r'^ration/(?P<pk>[0-9]+)/delete$', views.RationDelete.as_view(), name='ration-delete'),

      url(r'^distributor/(?P<pk>[0-9]+)/$', views.DistributorUpdate.as_view(), name='distributor-update'),
         url(r'^distributor/(?P<pk>[0-9]+)/delete$', views.DistributorDelete.as_view(), name='distributor-delete'),
]

urlpatterns += staticfiles_urlpatterns()
