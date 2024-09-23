from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'quotes_page', views.quotes_page, name='quotes_page'),
    path(r'show_all', views.show_all, name='show_all'),
    path(r'about', views.about, name='about'),

]