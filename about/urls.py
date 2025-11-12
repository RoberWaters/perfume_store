from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.about_page, name='about'),
    path('faq/', views.faq_page, name='faq'),
    path('blog/', views.blog_page, name='blog'),
    path('contact/', views.contact_page, name='contact'),
]