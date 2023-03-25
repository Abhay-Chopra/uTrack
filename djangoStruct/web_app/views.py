from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
# Create your views here.

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
