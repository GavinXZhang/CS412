from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Profile
from django.urls import reverse
from typing import Any
from django.views.generic.detail import DetailView


class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'Profile' # how to find the data in the template file
    def get_context_data(self, **kwargs):
        # Get the default context data from ListView
        context = super().get_context_data(**kwargs)
        
        # Add status messages for each profile
        profiles = context['Profile']
        for profile in profiles:
            # Fetch status messages associated with the profile
            profile.status_messages = StatusMessage.objects.filter(Profile=profile).order_by('-TimeStamp')
        return context

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # superclass context data
        context = super().get_context_data(**kwargs)
        return context


    def get_success_url(self) -> str :
        return reverse('show_all')
class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # superclass context data
        context = super().get_context_data(**kwargs)
        pk = self.kwarg['pk']
        Profile = Profile.objects.get(pk=pk)
        context['Profile'] = Profile
        return context
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # print(article)
        form.instance.Profile = profile
        return super().form_valid(form)


    def get_success_url(self) -> str :
        return reverse('show_all')

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'].status_messages = StatusMessage.objects.filter(Profile=profile).order_by('-TimeStamp')
        context['friends'] = profile.get_friends()

        return context
class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # Get profile IDs from the URL parameters
        profile_pk = self.kwargs.get('pk')
        other_pk = self.kwargs.get('other_pk')

        # Retrieve the Profile instances
        profile = get_object_or_404(Profile, pk=profile_pk)
        other_profile = get_object_or_404(Profile, pk=other_pk)

        # Attempt to add other_profile as a friend to profile
        profile.add_friend(other_profile)

        # Redirect back to the profile detail page
        return redirect('profile_detail', pk=profile_pk)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Add friend suggestions to the context
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Add the news feed to the context
        context['news_feed'] = profile.get_news_feed()
        return context