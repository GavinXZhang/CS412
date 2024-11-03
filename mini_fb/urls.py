from django.urls import path
from .views import * # our view class definition 
from .forms import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('show_all/<int:pk>/create_StatusMessage', CreateStatusMessageView.as_view(), name='Create_Message'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/add_friend/<int:other_pk>', CreateFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('profile/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('login/',auth_views.LoginView.as_view(template_name ='mini_fb/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'mini_fb/logout.html'), name='logout'),


    ]