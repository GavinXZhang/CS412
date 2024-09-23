from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .quotes import quotes
import time
import random
import os
# def home(request):


#     response_text= '''
#     Hello world!
#     ''' 
#     return HttpResponse(response_text)

image_folder = os.path.join('static','images')
image_filenames = os.listdir(image_folder)
def home(request):
    '''a function to fo work on an html template'''
    #template for response
    template_name = "quotes/home.html"

    context= {
        'letter1':random.choice(quotes),
        'picture' : random.choice(image_filenames),
    }


    return render(request, template_name, context)

def quotes_page(request):
    '''a function to fo work on an html template'''
    #template for response
    template_name = "quotes/quotes_page.html"

    context= {
        'current_time' : time.ctime()
    }


    return render(request, template_name, context)

def show_all(request):
    '''a function to fo work on an html template'''
    #template for response
    template_name = "quotes/show_all.html"

    context= {
        'q' : quotes,
        'imag': image_filenames
    }


    return render(request, template_name, context)

def about(request):
    '''a function to fo work on an html template'''
    #template for response
    template_name = "quotes/about.html"

    context= {
        'pic' : random.choice(image_filenames),
        'current_time' : time.ctime()
    }


    return render(request, template_name, context)