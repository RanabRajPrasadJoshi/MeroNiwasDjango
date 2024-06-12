from django.urls import path
from . import views



urlpatterns = [
   path('', views.show_product, name='home'),
   path('ContactUs/', views.show_product, name='ContactUs'),
   
    
]
