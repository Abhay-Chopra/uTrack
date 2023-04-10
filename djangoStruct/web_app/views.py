# Imports from base django
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.models import update_last_login
# Imports from django rest framework
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
# Imports from other files in the django project
from .models import *
from .serializer import *


# Creates a user instance
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'user': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Returns an authentication token to valid users
class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if not user.groups.filter(name=self.request.data.get('group')).exists():
            return HttpResponseForbidden('You are not allowed to access this resource')
        else:
            update_last_login(None, user)
            token, _ = Token.objects.get_or_create(user=user)  # _ discards the boolean value
            return Response({"status":status.HTTP_200_OK, 'token': token.key})


class CheckInSystemView(APIView):
    serializer_class = TrackedSessionsSerializer
    # TODO: Have this available to authenticated users only (leave this for now, come back after features are implemented)
    permission_classes = [AllowAny]

    def get(self, request, tracked_username):
        queryset = TrackedSessions.objects.filter(tracked_username=tracked_username)
        # Returns a 404 Response if there are no entries for the user
        if not queryset.exists():
            return Response({'error': 'No entries for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # We first filter to get all sessions from a user
        all_sessions = TrackedSessions.objects.filter(tracked_username=self.request.data.get('tracked_username'))
        # We then just get the newest created session that is 'ongoing' => Assuming only one ongoing session at a time
        instance = all_sessions.get(check_out_time=None)
        instance.check_out_time = self.request.data.get('check_out_time')
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckOutView(APIView):
    serializer_class = TrackedSessionsSerializer
    # TODO: Have this available to authenticated users only (leave this for now, come back after features are implemented)
    permission_classes = [AllowAny]
    
    def get(self, request, tracked_username):
        queryset = TrackedSessions.objects.filter(tracked_username=tracked_username).filter(check_out_time__isnull=True)
        # Returns a 404 Response if there are no ongoing sessions (i.e. sessions without an endtime)
        if not queryset.exists():
            return Response({'error': 'No ongoing sessions found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, many=True)
        return Response({'facility_id':serializer.data[0]['facility_id'],'check_in_time':serializer.data[0]['check_in_time']}, status=status.HTTP_200_OK)

    def delete(self, request, tracked_username):
        queryset = TrackedSessions.objects.filter(tracked_username=tracked_username).filter(check_out_time__isnull=True)
        # Returns a 404 Response if there are no ongoing sessions (i.e. sessions without an endtime)
        if not queryset.exists():
            return Response({'error': 'No ongoing sessions found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        # Deleting the ongoing session
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
########################################################

###### VIEWS THAT HANDLE GENERAL DATA ######


# Retrieves all the users in the group, "Tracked" usergroup
class AllUsersView(APIView):
    # could pass a parameter to specify which type of users we want

    def get(self, request):
        queryset = User.objects.filter(groups__name='Tracked')
        seralizer = UserSerializer(queryset, many=True)
        return Response(seralizer.data, status=status.HTTP_200_OK)


# Retrieves all the classes in the database
class AllClassesView(APIView):
    def get(self, request):
        all_classes = Class.objects.all()
        serializer = ClassSerializer(all_classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieves all the intramurals in the database
class AllIntramuralsView(APIView):
    def get(self, request):
        all_intramurals = Intramural.objects.all()
        serializer = IntramuralSerializer(all_intramurals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieves all the equipment in the database
class AllEquipmentView(APIView):
    def get(self, request):
        all_equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(all_equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieves all the facilities in the database
class AllFacilitiesView(APIView):
    def get(self, request):
        all_facilities = ActiveLivingFacility.objects.all()
        serializer = ActiveLivingFacilitySerializer(all_facilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


######################################################

###### VIEWS THAT HANDLE USER-SPECIFIC DATA ######


# Handles users' classes
class UserClassesView(APIView):
    serializer_class = EnrolledIn
    permission_classes = [AllowAny]

    # Retrieve the user's classes
    def get(self, request, username):
        # Returns a single object
        valid_user = get_object_or_404(User, pk=username)

        # Returns a set of objects
        queryset = EnrolledIn.objects.filter(username=valid_user)

        # # Validate its existence 
        # if not queryset.exists():  # not really necessary, if non-existent, no data is would be returned
        #     return Response({'error': 'No entries for this user.'}, status=status.HTTP_404_NOT_FOUND)

        class_ids = [enrollment.class_id for enrollment in queryset]
        classes = Class.objects.filter(class_id__in=class_ids)

        # many=True as it serializes a collection of objects
        serializer = ClassSerializer(classes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Allow the user to enroll in a class
    def post(self, request, username):
        # Get the user and class_id from the request data
        user = get_object_or_404(User, pk=username)
        class_id = request.data.get('class_id')

        # Check if the class exists
        class_obj = get_object_or_404(Class, class_id=class_id)

        # Check if the user is already enrolled in the class
        if EnrolledIn.objects.filter(username=user, class_id=class_obj).exists():
            return Response({'error': 'User already enrolled in this class.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new EnrolledIn object
        enrollment = EnrolledIn(username=user, class_id=class_obj)

        # Serialize and save the EnrolledIn object
        serializer = EnrolledInSerializer(data=enrollment.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handles users' intramurals
class UserIntramuralsView(APIView):
    serializer_class = CompetesIn
    permission_classes = [AllowAny]

    # Retrieve the user's intramurals
    def get(self, request, tracked_username):
        # Returns a single object
        valid_user = get_object_or_404(User, pk=tracked_username)

        # Returns a set of objects
        queryset = CompetesIn.objects.filter(tracked_username=valid_user)

        intramural_ids = [intramural.id for intramural in queryset]
        intramurals = Intramural.objects.filter(intramural_id__in=intramural_ids)

        # many=True as it serializes a collection of objects
        serializer = IntramuralSerializer(intramurals, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Allow the user to enroll in an intramural tournament
    def post(self, request, username):
        # Get the user and intramural_id from the request data
        user = get_object_or_404(User, pk=username)
        intramural_id = request.data.get('intramural_id')

        # Check if the intramural exists
        intramural_obj = get_object_or_404(Intramural, intramural_id=intramural_id)

        # Check if the user is already enrolled in the intramural
        if CompetesIn.objects.filter(tracked_username=user, intramural_id=intramural_obj).exists():
            return Response({'error': 'User already enrolled in this intramural.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new CompetesIn object
        competes = CompetesIn(tracked_username=user, intramural_id=intramural_obj)

        # Serialize and save the CompetesIn object
        serializer = CompetesInSerializer(data=competes.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handles users' equipment
class UserEquipmentView(APIView):
    serializer_class = RentsEquipment
    permission_classes = [AllowAny]

    # Retrieve the user's equipment
    def get(self, request, username):
        # Returns a single object
        valid_user = get_object_or_404(User, pk=username)

        # Returns a set of objects
        queryset = RentsEquipment.objects.filter(username=valid_user)

        equipment_ids = [equipment.id for equipment in queryset]
        equipments = Equipment.objects.filter(equipment_id__in=equipment_ids)

        # many=True as it serializes a collection of objects
        serializer = EquipmentSerializer(equipments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Allow the user to rent equipment
    def post(self, request, username):
        # Get the user and intramural_id from the request data
        user = get_object_or_404(User, pk=username)
        equipment_id = request.data.get('equipment_id')  # just realized inputting ids wouldn't be easy for users

        # Check if the intramural exists
        equipment_obj = get_object_or_404(Equipment, equipment_id=equipment_id)

        # Check if the user has already rented the equipment
        if RentsEquipment.objects.filter(username=user, equipment_id=equipment_obj).exists():
            return Response({'error': 'User has already rented this equipment.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new RentsEquipment object
        rents = RentsEquipment(username=user, equipment_id=equipment_obj)

        # Serialize and save the RentsEquipment object
        serializer = RentsEquipmentSerializer(data=rents.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Handles user's facilities
class UserFacilitiesView(APIView):
    serializer_class = UsesFacility
    permission_classes = [AllowAny]

    # Retrieve the user's used facilities
    def get(self, request, tracked_username):
        # Returns a single object
        valid_user = get_object_or_404(User, pk=tracked_username)

        # Returns a set of objects
        queryset = UsesFacility.objects.filter(tracked_username=valid_user)

        faciliy_ids = [facility.id for facility in queryset]
        facilites = ActiveLivingFacility.objects.filter(facility_id__in=faciliy_ids)
        
        # many=True as it serializes a collection of objects
        serializer = ActiveLivingFacilitySerializer(facilites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # No post or delete as the user shouldn't be allowed to modify the facilities he's used


######################################################