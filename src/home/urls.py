from django.urls import path
from . import views



urlpatterns = [
   path('', views.show_product, name='home'),
   path('ContactUs/', views.show_contactus, name='ContactUs'),
   path('Product/', views.search, name='search'),
   path('Login/', views.show_login, name='login'),
   path('Register/', views.show_selectRegister, name='selectregister'),
   path('RegisterBroker/', views.show_registerbroker, name='registerbroker'),
   
    
]
