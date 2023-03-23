from django.shortcuts import render
from django.http import HttpResponse

# Views are just a function which gets a request and returns a response (called actions in other architectures)
# Mapping of a view to a URL should take place so that each time a request is made to a URL, a particular function (view) is called
def home(request):
    '''
    Recieves a HTTP Request, and returns an instance of a HTTP Response
    '''
    return render(request, 'homepage.html')

def test_function(request):
    return HttpResponse('Test Response')