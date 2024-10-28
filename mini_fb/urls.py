from django.urls import path
from .views import * # our view class definition 
from .forms import *

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('show_all/<int:pk>/create_StatusMessage', CreateStatusMessageView.as_view(), name='Create_Message'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/add_friend/<int:other_pk>', CreateFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),

    ]