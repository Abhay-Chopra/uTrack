# Imports from base django
from django.shortcuts import render
from django.shortcuts import get_object_or_404
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


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
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


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    # post method for the register endpoint
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # returns a Http Response instance
        return Response({"user":UserSerializer(user, context=self.get_serializer_context()).data})


########################################################################


# If this make sense we could use it to register a new user utilizing UserRegistrationSerializer
# instead of RegisterSerializer
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

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


# If this make sense we could use it to log in users utilizing UserLoginSerializer
# instead of LoginSerializer
class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)  # _ discards the boolean value
        return Response({'token': token.key})


# Retrieves all the classes a Tracked user is enrolled in.
class TrackedEnrolledClassesView(APIView):

    def get(self, request, tracked_id):
        tracked = get_object_or_404(Tracked, pk=tracked_id)
        enrolled_in = EnrolledIn.objects.filter(username=tracked)

        class_ids = [enrollment.class_id_id for enrollment in enrolled_in]
        classes = Class.objects.filter(id__in=class_ids)

        serializer = ClassSerializer(classes, many=True)

        return Response(serializer.data)


# Allows a Tracked user to enroll in a class
class EnrolledInCreateAPIView(generics.CreateAPIView):

    queryset = EnrolledIn.objects.all()
    serializer_class = EnrolledInSerializer

    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        tracked_id = self.request.data.get('tracked_id')
        no_of_classes = self.request.data.get('no_of_classes')

        # Validate inputs
        if not class_id or not tracked_id or not no_of_classes:
            raise ValidationError("Please provide class_id, tracked_id, and no_of_classes.")

        tracked = get_object_or_404(Tracked, pk=tracked_id)
        class_ = get_object_or_404(Class, pk=class_id)

        # Check if user is already enrolled in the class
        if EnrolledIn.objects.filter(username=tracked, class_id=class_).exists():
            raise ValidationError("User is already enrolled in this class.")

        # Create enrollment
        enrollment = serializer.save(username=tracked, class_id=class_, no_of_classes=no_of_classes)

        return enrollment


# Allows a user to rent equipment
class EquipmentRentalsView(generics.CreateAPIView):

    serializer_class = EquipmentRentalsSerializer

    def post(self, request, *args, **kwargs):
        # Get the user making the request
        user = request.user

        # Get the rental data from the request data
        rental_data = request.data

        # Validate the rental data
        serializer = EquipmentRentalsSerializer(data=rental_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the equipment rental instance to update
        facility_id = rental_data.get('facility_id')
        name = rental_data.get('name')
        try:
            equipment_rental = EquipmentRentals.objects.get(facility_id=facility_id, name=name)
        except EquipmentRentals.DoesNotExist:
            return Response({'error': 'Equipment rental not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is allowed to rent equipment
        if not user.tracked:
            return Response({'error': 'User is not a Tracked user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rented the equipment
        if equipment_rental.tracked.filter(username=user.tracked).exists():
            return Response({'error': 'User has already rented this equipment.'}, status=status.HTTP_400_BAD_REQUEST)

        # Rent the equipment
        equipment_rental.tracked.add(user.tracked)
        equipment_rental.save()

        # Return a success response
        return Response({'success': 'Equipment rental added successfully.'}, status=status.HTTP_201_CREATED)


class CompetesIntramuralView(generics.CreateAPIView):
    serializer_class = IntramuralsSerializer
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
            return Response({'message': 'User is already enrolled in the tournament.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the facility is the same for the intramural tournament and the tracked user
        if tracked_user.facility_usage_set.first().facility_id != intramural.facility_id:
            return Response({'message': 'User is not authorized to compete in this intramural tournament.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create a new CompetesIn object to store the enrollment information
        new_competitor = CompetesIn(tracked=tracked_user, intramural_id=intramural)
        new_competitor.save()

        return Response({'message': 'User has been successfully enrolled in the tournament.'}, status=status.HTTP_201_CREATED)


