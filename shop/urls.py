from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='shophome'),
    path('about/', views.about, name='aboutus'),
    path('contact/', views.contact, name='contactus'),
    path('search/', views.search, name='search'),
    path('tracker/', views.tracker, name='trackingstatus'),
    path('products/<int:id>', views.productview, name='productview'),
    path('checkout/', views.checkout, name='checkout'),
]