from django.urls import path
from . import views, admin_views

app_name = 'shop'

urlpatterns = [
    # URLs públicas
    path('', views.home, name='home'),
    path('perfumes/', views.perfume_list, name='perfume_list'),
    path('perfume/<slug:slug>/', views.perfume_detail, name='perfume_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:perfume_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),

    # Panel de Administración
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/perfumes/', admin_views.admin_perfumes_list, name='admin_perfumes_list'),
    path('admin-panel/perfumes/add/', admin_views.admin_perfume_add, name='admin_perfume_add'),
    path('admin-panel/perfumes/<int:pk>/edit/', admin_views.admin_perfume_edit, name='admin_perfume_edit'),
    path('admin-panel/perfumes/<int:pk>/delete/', admin_views.admin_perfume_delete, name='admin_perfume_delete'),
    path('admin-panel/orders/', admin_views.admin_orders_list, name='admin_orders_list'),
    path('admin-panel/orders/<int:pk>/', admin_views.admin_order_detail, name='admin_order_detail'),
]
