from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from web_app.views import *

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/auth/login/', UserLoginView.as_view()),
	path('api/auth/register/', UserRegistrationView.as_view()),
	path('api/get_Users/', AllUsersView.as_view()),
	path('api/get_Checkins/<str:tracked_username>/', CheckInSystemView.as_view()),
    path('api/get_Checkins/last/<str:tracked_username>/', CheckOutView.as_view())
]