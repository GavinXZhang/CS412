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
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login


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
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            # Initialize both forms with POST data
            user_form = UserCreationForm(request.POST)
            profile_form = CreateProfileForm(request.POST, request.FILES)

            # Validate both forms
            if user_form.is_valid() and profile_form.is_valid():
                # Save the user and log them in
                user = user_form.save()
                login(request, user)

                # Attach the user to the profile and save
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                # Redirect to success URL
                return redirect(reverse('show_all'))
            else:
                # If either form is invalid, re-render the template with error messages
                context = self.get_context_data()
                context['user_form'] = user_form
                context['form'] = profile_form
                return render(request, self.template_name, context)
        
        # For GET requests, just use the superclass dispatch method
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure both forms are in the context data for rendering
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context


    def get_success_url(self) -> str :
        return reverse('show_all')
    def get_login_url(self) -> str:
        return reverse('login')
    def form_valid(self, form):
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
        # attach user to form instance (Article object):
        form.instance.user = user
        return super().form_valid(form)



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
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
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
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
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
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
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
    def get_object(self):
        return Profile.objects.get(user=self.request.user)