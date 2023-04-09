from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate


### SERIALIZERS FOR EACH MODEL ###

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class AttendantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendant
        fields = ['username']


class VerifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verifier
        fields = ['username']


class CoachSerializer(serializers.ModelSerializer):
    username = VerifierSerializer()
    class Meta:
        model = Coach
        fields = ['username', 'dinos_team']


class TrackedSerializer(serializers.ModelSerializer):
    username = AttendantSerializer()
    class Meta:
        model = Tracked
        fields = ['username', 'goal_hours']


class HoursReportSerializer(serializers.ModelSerializer):
    username = TrackedSerializer()
    class Meta:
        model = HoursReport
        fields = ['username', 'hours']


class ApplicationReviewerSerializer(serializers.ModelSerializer):
    verifier_username = VerifierSerializer()
    tracked_username = TrackedSerializer()
    hours = HoursReportSerializer()  # need to reference hours, not the primary key
    class Meta:
        model = ApplicationReviewer
        fields = ['verifier_username', 'tracked_username', 'hours']


class OverseesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oversees
        fields = ['verifier_username', 'tracked_username']


class TrackedSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedSessions
        fields = ['tracked_username', 'facility_id', 'check_in_time', 'check_out_time']


class AlumnusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnus
        fields = ['username']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username']


class DinosMemberSerializer(serializers.ModelSerializer):
    username = StudentSerializer()
    class Meta:
        model = DinosMember
        fields = ['username', 'dinos_team']


class ActiveLivingFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLivingFacility
        fields = ['facility_id']


class WorksAtSerializer(serializers.ModelSerializer):
    username = AttendantSerializer()
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = WorksAt
        fields = ['username', 'facility_id']


class FacilityUsageSerializer(serializers.ModelSerializer):
    username = TrackedSerializer()
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = FacilityUsage
        fields = ['username', 'facility_id']


class ChecksInSerializer(serializers.ModelSerializer):
    attendant_username = AttendantSerializer()
    tracked_username = TrackedSerializer()
    class Meta:
        model = ChecksIn
        fields = ['attendant_username', 'tracked_username']


class LooksAtSerializer(serializers.ModelSerializer):
    verifier_username = VerifierSerializer()
    tracked_username = TrackedSerializer()
    hours = HoursReportSerializer()
    class Meta:
        model = LooksAt
        fields = ['verifier_username', 'tracked_username', 'hours']


class IntramuralsSerializer(serializers.ModelSerializer):
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = Intramurals
        fields = ['intramural_id', 'intramural_team', 'facility_id']


class ClassSerializer(serializers.ModelSerializer):
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = Class
        fields = ['class_id', 'facility_id']


class EnrolledInSerializer(serializers.ModelSerializer):
    username = TrackedSerializer()
    class_id = ClassSerializer()
    class Meta:
        model = EnrolledIn
        # doesn't make sense to have no. of classes if there's a single class_id
        fields = ['username', 'class_id']


class EquipmentRentalsSerializer(serializers.ModelSerializer):
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = EquipmentRentals
        fields = ['facility_id', 'name', 'cost']


class CompetesInSerializer(serializers.ModelSerializer):
    tracked = TrackedSerializer()
    intramural_id = IntramuralsSerializer()
    class Meta:
        model = CompetesIn
        fields = ['tracked', 'intramural_id']



######################################################################


### SERIALIZERS FOR VIEWS THAT ALLOW USERS TO CREATE NEW INSTANCES OF A DATA MODEL ###


######################################################################


### TODO: SERIALIZERS FOR VIEWS THAT RETURN A LIST OF INSTANCES OF A DATA MODEL ###

# need to include the subset of fields that are relevant to the user in the serializer

######################################################################


### SERIALIZERS FOR VIEWS THAT REQUIRE AUTHORIZATION OR AUTHENTICAION ###

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=8)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, max_length=24)
    email = serializers.CharField(write_only=True, required=True, max_length=40)
    first_name = serializers.CharField(write_only=True, required=True, max_length=20)
    last_name = serializers.CharField(write_only=True, required=True, max_length=20)
    # making sure the user is given a usergroup
    group = serializers.CharField(write_only=True, required=True, max_length=10)
    class Meta:
        model = User
        fields = ['username','email', 'password', 'group', 'first_name', 'last_name']

    #TODO: Handle errors when user group doesn't exist, or when username is already taken
    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        # user_type = validated_data.pop('user_type')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        
        user.set_password(password)
        user.save()
        # adding user to a user group
        group = Group.objects.get(name=validated_data.pop('group'))
        user.groups.add(group)
        return user

    ########################################################################################### DEPRACATED
    def validate_user_type(self, value):
        user_types = ['tracked', 'verifier', 'attendant']
        if value not in user_types:
            raise ValidationError(f'User type must be one of the following: {user_types}')
        return value
    ###########################################################################################

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=24, write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if not user.is_active:
            raise ValidationError("Inactive User")
        if not user:
            raise ValidationError("Invalid login credentials")

        return user

