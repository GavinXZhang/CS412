from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse
from typing import Any


class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'Profile' # how to find the data in the template file
    def get_message(self):
        message = StatusMessage.objects.filter(Profile = self).order_by('-TimeStamp')
        return message
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