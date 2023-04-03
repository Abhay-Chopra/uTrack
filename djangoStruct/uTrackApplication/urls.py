from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from web_app.views import *

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', ReactView.as_view()),
	path('api/auth/login/', LoginView.as_view()),
	path('api/auth/register/', RegsiterView.as_view())
]
