from django.urls import path
from .views import * # our view class definition 
from .forms import *

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('show_all/<int:pk>/create_StatusMessage', CreateStatusMessageView.as_view(), name='Create_Message'),
    
    ]