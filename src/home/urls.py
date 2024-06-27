from django.urls import path
from . import views



urlpatterns = [
   path('', views.show_product, name='home'),
   path('ContactUs/', views.show_contactus, name='ContactUs'),
   path('Product/', views.search, name='search'),
   path('Login/', views.show_login, name='login'),
   path('Register/', views.show_selectRegister, name='selectregister'),
   path('RegisterBroker/', views.show_registerBroker, name='registerbroker'),
   path('RegisterRegular/', views.show_registerRegular, name='registerregular'),
   path('LoginSuccess/', views.show_successLogin, name='successLogin'),
   path('verify_emailregular/', views.verify_emailregular, name='verify_emailregular'),
   path('verify_emailbroker/', views.verify_emailbroker, name='verify_emailbroker'),
   path('logout/', views.show_logout, name='logout'),
   
    
]
