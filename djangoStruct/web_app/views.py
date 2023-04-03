# Imports from base django
from django.shortcuts import render
from django.contrib.auth.models import update_last_login
# Imports from django rest framework
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
# Imports from other files in the django project
from .models import *
from .serializer import *

class ReactView(APIView):
    serializer_class = ReactSerializer
    
    def get(self, request):
        print("get received")
        detail = [{"name": detail.name, "detail": detail.detail}
                  for detail in React.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def put(self, request):
        # handle PUT requests here
        pass
    
    def delete(self, request):
        # handle DELETE requests here
        pass
    
    def head(self, request):
        # handle HEAD requests here
        pass
    
    def patch(self, request):
        # handle PATCH requests here
        pass
    
    def options(self, request):
        # handle OPTIONS requests here
        pass


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    # post method for the login endpoint
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # logging the user in (using django sessions)
        update_last_login(None, user)
        
        # Creating a authentication token and having the token expire after one hour
        token, created = Token.objects.get_or_create(user=user)
        return Response({"status":status.HTTP_200_OK, "token":token.key})


class RegsiterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    # post method for the register endpoint
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # returns a Http Response instance
        return Response({"user":UserSerializer(user, context=self.get_serializer_context()).data})
        
        
# Views are just a function which gets a request and returns a response (called actions in other architectures)
# Mapping of a view to a URL should take place so that each time a request is made to a URL, a particular function (view) is called
def test(request):
    '''
    Recieves a HTTP Request, and returns an instance of a HTTP Response
    '''
    # This function is returning a template, which is a depreciated practice, can dynamically build the HTML File in the front end insead
    return render(request, 'homepage.html')