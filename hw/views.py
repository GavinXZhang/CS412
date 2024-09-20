from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# def home(request):


#     response_text= '''
#     Hello world!
#     ''' 
#     return HttpResponse(response_text)

def home(request):
    '''a function to fo work on an html template'''
    #template for response
    template_name = "hw/home.html"

    context= {
        'current_time' : time.ctime(),
        'letter1' : chr(random.randint(65,90)),
        'letter2' : chr(random.randint(65,90)),
    }


    return render(request, template_name, context)

def about(request):
    '''a function to fo work on an html template'''
    #template for response
    template_name = "hw/about.html"

    context= {
        'current_time' : time.ctime()
    }


    return render(request, template_name, context)