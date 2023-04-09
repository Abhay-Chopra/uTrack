from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from web_app.views import *

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/auth/login/', UserLoginView.as_view()),
	path('api/auth/register/', UserRegistrationView.as_view()),
	path('api/get_Users/', AllUsersView.as_view()),
	path('api/Checkins/', CheckInSystemView.as_view()),
	path('api/get_Checkins/<str:tracked_username>/', CheckInSystemView.as_view()),
    path('api/get_Checkins/last/<str:tracked_username>/', CheckOutView.as_view()),
    path('api/get_Classes/<str:tracked_username>', UserClassesView.as_view()),
    path('api/get_Equipment/<str:tracked_username>', UserEquipmentView.as_view()),
    path('api/get_Intramurals/<str:tracked_username>', UserIntramuralsView.as_view())
]