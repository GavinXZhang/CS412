from django.urls import path 
from . import views

app_name = 'gacha'

urlpatterns = [
    path('',views.index, name = 'index'),
    path('spin/', views.spin, name= 'spin')
]