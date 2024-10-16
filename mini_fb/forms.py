from django import forms
from .models import *
class CreateProfileForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Profile
        fields = ['FirstName','LastName','City','Email','ProfileImage']
class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['Message']