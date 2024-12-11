from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.HomePageView, name='home'),
    path('event_list/', views.CalendarEventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', views.CalendarEventDetailView.as_view(), name='event-detail'),
    path('add-event/', views.CalendarEventCreateView.as_view(), name='add-event'),
    path('event/<int:pk>/delete/', views.CalendarEventDeleteView.as_view(), name='event-delete'),
    path('reminder/add/', views.ReminderCreateView.as_view(), name='reminder-create'),
    path('reminder/<int:pk>/', views.ReminderDetailView.as_view(), name='reminder-detail'),  # Add this line
    path('reminder/<int:pk>/delete/', views.ReminderDeleteView.as_view(), name='reminder-delete'),
    path('calllog/add/', views.CallLogCreateView.as_view(), name='calllog-create'),
    path('calllog/<int:pk>/delete/', views.CallLogDeleteView.as_view(), name='calllog-delete'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

]
