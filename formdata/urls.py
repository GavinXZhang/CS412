from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.show_form, name='form_data'),
    path(r'submit', views.submit, name = "submit"),
    

]