# blog/forms.py

from django import forms
from .models import *

class CreateCommentForm(forms.ModelForm):
    '''A form to create Comment data.'''

    class Meta:
        '''associate this form witht he Comment model'''
        model = Comment
        # fields = ['article', 'author', 'text', ]
        # remove the article because we want to do this automagically
        fields = ['author', 'text', ]
class CreateArticleForm(forms.ModelForm):
    '''A form to create a new Article'''

    class Meta:
        model = Article 
        fields = ['author', 'title','text','image_file']

    def form_valid(self,form):
        '''Add some debugging statements'''
        print(f'CreateArticleView.form_valid: form.cleaned_data= {form.cleaned_data}')

        return super().form_valid(form)