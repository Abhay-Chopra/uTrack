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
            return Response({"status":status.HTTP_200_OK, 'token': token.key, 'name': f"{user.first_name} {user.last_name}", 'ucid':user.username})


class CheckInSystemView(APIView):
    serializer_class = TrackedSessionsSerializer
    # TODO: Have this available to authenticated users only (leave this for now, come back after features are implemented)
    permission_classes = [AllowAny]

    def get(self, request):
        tracked_username = request.GET.get('tracked_username', None)
        # Confirming that the endpoint got a username
        if not tracked_username:
            return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = TrackedSessions.objects.filter(tracked_username=tracked_username)
        
        # Returns a 404 Response if there are no entries for the user
        if not queryset.exists():
            return Response({'error': 'No entries for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, many=True)
        
        response_data = []
        for each in serializer.data:
            date_str = each['check_in_time']
            time_in_facility = each['time_in_facility']
            # Making sure we don't return any redundant session entries
            if time_in_facility == '0 hours, 0 minutes' or not time_in_facility:
                continue
            response_data.append({'facility_id':each['facility_id'],'date':datetime.fromisoformat(date_str[:-1]).date(), 'time_in_facility':time_in_facility})

        # Returning the response_data array that was created
        return Response(response_data, status=status.HTTP_200_OK)

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


# Handles all the classes in the database
class AllClassesView(APIView):

    # Retrieve all the classes
    def get(self, request):
        all_classes = Class.objects.all()
        serializer = ClassSerializer(all_classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new class
    def post(self, request):
        # Get the info from the request data
        class_id = request.data.get('class_id')
        facility_id = request.data.get('facility_id')

        # Check if the class exists
        class_obj = Class.objects.filter(class_id=class_id)
        if class_obj.exists():
            return Response({'error': 'Class already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new class object
        class_obj = Class(class_id=class_id, facility_id=facility_id)

        # Serialize and save the Class object
        serializer = ClassSerializer(data=class_obj.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a class
    def delete(self, request):
        # Get and validate the Class
        class_id = request.data.get('class_id')
        class_obj = Class.objects.filter(class_id=class_id)
        if not class_obj.exists():
            return Response({'error': 'No such class exists.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the class
        class_obj.delete()

        return Response({'success': 'Class deleted.'}, status=status.HTTP_204_NO_CONTENT)


# Handles all the intramurals in the database
class AllIntramuralsView(APIView):

    # Retrieve all the intramurals
    def get(self, request):
        all_intramurals = Intramural.objects.all()
        serializer = IntramuralSerializer(all_intramurals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new intramural
    def post(self, request):
        # Get the info from the request data
        intramural_id = request.data.get('intramural_id')
        intramural_name = request.data.get('intramural_name')
        facility_id = request.data.get('facility_id')

        # Check if the intramural exists
        intramural_obj = Intramural.objects.filter(intramural_id=intramural_id)
        if intramural_obj.exists():
            return Response({'error': 'Intramural already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new intramural object
        intramural_obj = Intramural(intramural_id=intramural_id, intramural_name=intramural_name, facility_id=facility_id)

        # Serialize and save the Intramural object
        serializer = IntramuralSerializer(data=intramural_obj.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete an intramural
    def delete(self, request):
        # Get and validate the intramural
        intramural_id = request.data.get('intramural_id')
        intramural_obj = Intramural.objects.filter(intramural_id=intramural_id)
        if not intramural_obj.exists():
            return Response({'error': 'No such intramural exists.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the intramural
        intramural_obj.delete()

        return Response({'success': 'Intramural deleted.'}, status=status.HTTP_204_NO_CONTENT)


# Handles all the equipment in the database
class AllEquipmentView(APIView):

    # Retrieve all the equipment
    def get(self, request):
        all_equipment = Equipment.objects.all()
        serializer = EquipmentSerializer(all_equipment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create new equipment
    def post(self, request):
        # Get the info from the request data
        equipment_id = request.data.get('equipment_id')
        facility_id = request.data.get('facility_id')
        description = request.data.get('description')
        cost = request.data.get('cost')

        # Check if the equipment exists
        equipment_obj = Equipment.objects.filter(equipment_id=equipment_id)
        if equipment_obj.exists():
            return Response({'error': 'Equipment already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new equipment object
        equipment_obj = Equipment(equipment_id=equipment_id, facility_id=facility_id, description=description, cost=cost)

        # Serialize and save the Equipment object
        serializer = EquipmentSerializer(data=equipment_obj.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete equipment
    def delete(self, request):
        # Get and validate the equipment
        equipment_id = request.data.get('equipment_id')
        equipment_obj = Equipment.objects.filter(equipment_id=equipment_id)
        if not equipment_obj.exists():
            return Response({'error': 'No such equipment exists.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the equipment
        equipment_obj.delete()

        return Response({'success': 'Equipment deleted.'}, status=status.HTTP_204_NO_CONTENT)


# Handles all the facilities in the database
class AllFacilitiesView(APIView):

    # Retrieve all the facilites
    def get(self, request):
        all_facilities = ActiveLivingFacility.objects.all()
        serializer = ActiveLivingFacilitySerializer(all_facilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new facility
    def post(self, request):
        # Get the info from the request data
        facility_id = request.data.get('facility_id')
        facility_name = request.data.get('facility_name')

        # Check if the facility exists
        facility_obj = ActiveLivingFacility.objects.filter(facility_id=facility_id)
        if facility_obj.exists():
            return Response({'error': 'Facility already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new facility object
        facility_obj = ActiveLivingFacility(facility_id, facility_name=facility_name)

        # Serialize and save the facility object
        serializer = ActiveLivingFacilitySerializer(data=facility_obj.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a facility
    def delete(self, request):
        # Get and validate the facility
        facility_id = request.data.get('facility_id')
        facility_obj = ActiveLivingFacility.objects.filter(facility_id=facility_id)
        if not facility_obj.exists():
            return Response({'error': 'No such facility exists.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the facility
        facility_obj.delete()

        return Response({'success': 'Facility deleted.'}, status=status.HTTP_204_NO_CONTENT)


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

        # Validate its existence 
        if not queryset.exists():
            return Response({'error': 'No classes for this user.'}, status=status.HTTP_404_NOT_FOUND)

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

    # Allow the user to cease enrollment in a class
    def delete(self, request, username):
        # Get and validate the user
        valid_user = get_object_or_404(User, pk=username)

        # Get and validate the class
        class_id = request.data.get('class_id')
        class_obj = get_object_or_404(Class, class_id=class_id)

        # Get and validate the enrollment
        enrolled_in = EnrolledIn.objects.filter(username=valid_user, class_id=class_obj)  #
        if not enrolled_in.exists():
            return Response({'error': 'No enrollment for this user and class.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the enrollment
        enrolled_in.delete()

        return Response({'success': 'Enrollment deleted.'}, status=status.HTTP_204_NO_CONTENT)


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

        # Validate its existence 
        if not queryset.exists():
            return Response({'error': 'No intramurals for this user.'}, status=status.HTTP_404_NOT_FOUND)

        intramural_ids = [intramural.id for intramural in queryset]
        intramurals = Intramural.objects.filter(intramural_id__in=intramural_ids)

        # many=True as it serializes a collection of objects
        serializer = IntramuralSerializer(intramurals, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Allow the user to enroll in an intramural tournament
    def post(self, request, tracked_username):
        # Get the user and intramural_id from the request data
        user = get_object_or_404(User, pk=tracked_username)
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

    # Allow the user to cease inscription in an intramural
    def delete(self, request, tracked_username):
        # Get and validate the user
        valid_user = get_object_or_404(User, pk=tracked_username)

        # Get and validate the intramural
        intramural_id = request.data.get('intramural_id')
        intramural_obj = get_object_or_404(Intramural, intramural_id=intramural_id)

        # Get and validate the intramural inscription
        competes_in = CompetesIn.objects.filter(username=valid_user, intramural_id=intramural_obj)
        if not competes_in.exists():
            return Response({'error': 'No inscription for this user and intramural.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the inscription
        competes_in.delete()

        return Response({'success': 'Inscription deleted.'}, status=status.HTTP_204_NO_CONTENT)


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

        # Validate its existence 
        if not queryset.exists():
            return Response({'error': 'No equipment for this user.'}, status=status.HTTP_404_NOT_FOUND)

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

    # Allow the user to stop renting equipment
    def delete(self, request, username):
        # Get and validate the user
        valid_user = get_object_or_404(User, pk=username)

        # Get and validate the equipment
        equipment_id = request.data.get('equipment_id')
        equipment_obj = get_object_or_404(Equipment, equipment_id=equipment_id)

        # Get and validate the equipment renting
        rents_equipment = RentsEquipment.objects.filter(username=valid_user, equipment_id=equipment_obj)
        if not rents_equipment.exists():
            return Response({'error': 'No such equipment for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the equipment
        rents_equipment.delete()

        return Response({'success': 'Equipment deleted.'}, status=status.HTTP_204_NO_CONTENT)


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

        # Validate its existence 
        if not queryset.exists():
            return Response({'error': 'No facilites for this user.'}, status=status.HTTP_404_NOT_FOUND)

        facility_ids = [facility.id for facility in queryset]
        facilites = ActiveLivingFacility.objects.filter(facility_id__in=facility_ids)
        
        # many=True as it serializes a collection of objects
        serializer = ActiveLivingFacilitySerializer(facilites, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # No post or delete as the user shouldn't be allowed to modify the facilities he's used


######################################################

# Handle coach's user list
class OverseerView(APIView):
    serializer_class = OverseesSerializer
    permission_classes = [AllowAny]
    
    def get(self, request):
        verifier_username = request.GET.get('verifier_username', None)
        # Confirming that the endpoint got a username => which is a verifiers
        if not verifier_username:
            return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username=verifier_username)
        # Confirming that we have gotten a verfied viewer (given that the user only has one group)
        if user.groups.first().name == "Viewer":
            serializer = OverseesSerializer(verifier_username, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Reached here when usergroup is not as above
        return Response({'error': 'You are not a verified viewer!'}, status=status.HTTP_403_FORBIDDEN)