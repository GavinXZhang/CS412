from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def main(request):
    template_name = "restaurant/main.html"
    return render(request,'restaurant/main.html')
def order(request):
    template_name = "restaurant/order.html"
    return render(request,template_name)
def confirmation(request):
    "handle submission form read the data and generate a response."
    template_name = "restaurant/confirmation.html"
    
    

    #Read the form data into python variables, sending data is get, data in the form of a url.
    if request.POST:
        name = request.POST['name']
        #package it backup to be used in the response.
        context = {
            'name': name,
        }
        return render(request,template_name,context)

    #Get lands down here: no return statements!
    #Ok solution    
    # template_name = "formdata/form.html"
    # return render(request, template_name)

    # This is the best solution redirect to the correct url.
    return redirect("order")