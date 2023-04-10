from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from web_app.views import *

urlpatterns = [

	#HANDLING AUTHORIZATION AND AUTHENTICATION
	path('admin/', admin.site.urls),
	path('api/auth/login/', UserLoginView.as_view()),
	path('api/auth/register/', UserRegistrationView.as_view()),
    
	# HANDLING GENERAL DATA
	path('api/get_users/', AllUsersView.as_view()),    
	path('api/get_classes/', AllClassesView.as_view()),
    path('api/get_intramurals/', AllIntramuralsView.as_view()),
    path('api/get_equipment/', AllEquipmentView.as_view()),	
	
	# 
	path('api/Checkins/', CheckInSystemView.as_view()),
	path('api/get_Checkins/<str:tracked_username>/', CheckInSystemView.as_view()),
    path('api/get_Checkins/last/<str:tracked_username>/', CheckOutView.as_view()),
    
	# HANDLING USER-SPECIFIC DATA
    path('api/get_user_classes/<str:username>', UserClassesView.as_view()),
    path('api/get_user_intramurals/<str:tracked_username>', UserIntramuralsView.as_view()),
    path('api/get_user_equipment/<str:username>', UserEquipmentView.as_view())
]