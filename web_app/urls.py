from django.urls import path
from . import views

# URLConf
# this is a special variable that Django looks for, it will be an array of URL pattern objects
urlpatterns = [
    # the path function takes a URL, and a refrence to a views function and returns a URL pattern object
    path('', views.home, name='homepage'),
    path('test/', views.test_function) 
]