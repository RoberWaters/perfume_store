from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('perfumes/', views.perfume_list, name='perfume_list'),
    path('perfume/<slug:slug>/', views.perfume_detail, name='perfume_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:perfume_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
]
