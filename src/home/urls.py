from django.urls import path
from . import views



urlpatterns = [
   path('', views.index, name='home'),
   path('ContactUs/', views.show_contactus, name='ContactUs'),
   path('Product/', views.show_product, name='show_product'),
   path('AboutUs/', views.show_aboutUs, name='about_us'),
   path('ProductBroker/', views.show_productBroker, name='show_productBroker'),
   path('Login/', views.show_login, name='login'),
   path('Register/', views.show_selectRegister, name='selectregister'),
   path('RegisterBroker/', views.show_registerBroker, name='registerbroker'),
   path('RegisterRegular/', views.show_registerRegular, name='registerregular'),
   path('LoginSuccess/', views.show_successLogin, name='successLogin'),
   path('verify_emailregular/', views.verify_emailregular, name='verify_emailregular'),
   path('verify_emailbroker/', views.verify_emailbroker, name='verify_emailbroker'),
   path('logout/', views.show_logout, name='logout'),
   path('AddProduct/', views.show_AddProduct, name='AddProduct'),
   path('MyProduct/', views.show_MyProduct, name='MyProduct'),
   path('Profile/', views.show_profile, name='profile'),
   path('updateprofile/', views.update_profile, name='updateprofile'),
   path('product/<int:room_id>/', views.product_detail, name='product_detail'),
   path('updateproduct/<int:room_id>', views.show_updateProduct, name="updateproduct"),
   path('deleteProduct/<int:room_id>', views.show_deleteProduct, name="deleteProduct"),
   
    
]
