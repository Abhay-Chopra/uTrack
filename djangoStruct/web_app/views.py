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
    
    def get(self, request, tracked_username):
        queryset = TrackedSessions.objects.filter(tracked_username=tracked_username).filter(check_out_time__isnull=True)
        # Returns a 404 Response if there are no ongoing sessions (i.e. sessions without an endtime)
        if not queryset.exists():
            return Response({'error': 'No ongoing sessions found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, many=True)
        return Response({'facility_id':serializer.data[0]['facility_id'],'check_in_time':serializer.data[0]['check_in_time']}, status=status.HTTP_200_OK)


########################################################

###### VIEWS THAT HANDLE GENERAL DATA ######


# Retrieves all the users in the group, "Tracked" usergroup
class AllUsersView(APIView):
    # could pass a parameter to specify which type of users we want

    def get(self, request):
        queryset = User.objects.filter(groups__name='Tracked')
        seralizer = UserSerializer(queryset, many=True)
        return Response(seralizer.data, status=status.HTTP_200_OK)


class AllClassesView(APIView):
    pass


class AllIntramuralsView(APIView):
    pass


class AllEquipmentView(APIView):
    pass


######################################################

###### VIEWS THAT HANDLE USER-SPECIFIC DATA ######


# The classes a user participates in
class UserClassesView(APIView):
    serializer_class = EnrolledIn
    permission_classes = [AllowAny]

    # Retrieve the user's classes
    def get(self, request, username):
        # Returns a single object
        valid_user = get_object_or_404(User, pk=username)

        # Returns a queryset
        enrolled_in = EnrolledIn.objects.filter(username=valid_user)

        class_ids = [enrollment.class_id for enrollment in enrolled_in]
        classes = Class.objects.filter(id__in=class_ids)

        # many=True as it serializes a collection of objects
        serializer = ClassSerializer(classes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update the user's classes
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# The intramurals a user participates in
class UserIntramuralsView(APIView):

    serializer_class = CompetesIn
    permission_classes = [AllowAny]

    def get(self, request, tracked_username):
        queryset = CompetesIn.objects.filter(tracked_username=tracked_username)
        if not queryset.exists():
            return Response({'error': 'No entries for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# The equipment a user rents
class UserEquipmentView(APIView):

    serializer_class = RentsEquipment
    permission_classes = [AllowAny]

    def get(self, request, username):
        queryset = RentsEquipment.objects.filter(username=username)
        if not queryset.exists():
            return Response({'error': 'No entries for this user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


######################################################

#### VIEWS THAT UPDATE USER-SPECIFIC DATA IN THE DB ####

###TODO: INCORPORATE THESE VIEWS INTO THE ONES ABOVE
### TO REDUCE REDUNDANCY

# Allows a Tracked user to enroll in a class
class EnrolledInView(generics.CreateAPIView):

    queryset = EnrolledIn.objects.all()
    serializer_class = EnrolledInSerializer

    # TODO: any type of user should be able to register in classes
    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        username = self.request.data.get('username')

        # Validate inputs
        if not class_id or not username:
            raise ValidationError("Please provide class_id and username.")

        tracked = get_object_or_404(Tracked, pk=username)
        class_ = get_object_or_404(Class, pk=class_id)

        # Check if user is already enrolled in the class
        if EnrolledIn.objects.filter(username=tracked, class_id=class_).exists():
            raise ValidationError("User is already enrolled in this class.")

        # Create enrollment
        enrollment = serializer.save(username=tracked, class_id=class_)

        return enrollment


# Allows a user to compete in an intramural tournament
class CompetesInView(generics.CreateAPIView):
    serializer_class = IntramuralsSerializer
    second_serializer = CompetesInSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, intramural_id):
        intramural = Intramurals.objects.filter(intramural_id=intramural_id).first()
        if not intramural:
            raise ValidationError('Intramural tournament not found.')

        tracked_user = Tracked.objects.filter(username=request.user).first()
        if not tracked_user:
            raise ValidationError('Tracked user not found.')

        # Check if the user is already enrolled
        if CompetesIn.objects.filter(tracked=tracked_user, intramural_id=intramural).exists():
            return Response({'error': 'User is already enrolled in the tournament.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new CompetesIn object to store the enrollment information
        new_competitor = CompetesIn(tracked=tracked_user, intramural_id=intramural)
        new_competitor.save()

        return Response({'success': 'User has been successfully enrolled in the tournament.'}, status=status.HTTP_201_CREATED)


# Allows a user to rent equipment
class RentsEquipmentView(generics.CreateAPIView):

    serializer_class = RentsEquipmentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        rental_data = request.data

        # Validate the rental data
        serializer = RentsEquipmentSerializer(data=rental_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the equipment rental instance to update
        equipment_id = rental_data.get('equipment_id')
        try:
            equipment_rental = RentsEquipment.objects.get(equipment_id=equipment_id)
        except RentsEquipment.DoesNotExist:
            return Response({'error': 'Equipment rental not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is allowed to rent equipment
        if not user.tracked:  # look more into this
            return Response({'error': 'User is not a Tracked user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rented the equipment
        if equipment_rental.tracked.filter(username=user.tracked).exists():  # look more into this
            return Response({'error': 'User has already rented this equipment.'}, status=status.HTTP_400_BAD_REQUEST)

        # Rent the equipment
        equipment_rental.tracked.add(user.tracked)
        equipment_rental.save()

        # Return a success response
        return Response({'success': 'Equipment rental added successfully.'}, status=status.HTTP_201_CREATED)

