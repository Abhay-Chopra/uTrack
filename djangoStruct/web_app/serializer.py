from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate


### SERIALIZERS FOR EACH MODEL ###

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'firstName', 'lastName']


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
        fields = ['username', 'facility', 'check_in_time', 'check_out_time']


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
        fields = ['username', 'class_id', 'no_of_classes']


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


### TODO: SERIALIZERS FOR VIEWS THAT REQUIRE AUTHORIZATION OR AUTHENTICAION ###

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=8)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, max_length=24)
    email = serializers.CharField(write_only=True, required=True, max_length=40)
    first_name = serializers.CharField(write_only=True, required=True, max_length=20)
    last_name = serializers.CharField(write_only=True, required=True, max_length=20)

    class Meta:
        model = User
        fields = ['username','email', 'password', 'user_type', 'first_name', 'last_name']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user_type = validated_data.pop('user_type')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        user = User(email=email, user_type=user_type, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def validate_user_type(self, value):
        user_types = ['tracked', 'verifier', 'attendant']
        if value not in user_types:
            raise ValidationError(f'User type must be one of the following: {user_types}')
        return value


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


class RegisterSerializer(serializers.ModelSerializer):
    # these fields specify the data that is required from the incoming request to create a new user
    username = serializers.CharField(write_only=True, required=True, max_length=8)
    password = serializers.CharField(write_only=True, required=True, max_length=24)
    email = serializers.CharField(write_only=True, required=True, max_length=40)
    firstName = serializers.CharField(write_only=True, required=True, max_length=20)
    lastName = serializers.CharField(write_only=True, required=True, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'firstName', 'lastName')

        # since this is already specified in the first set of fields I think it is redundant
        extra_kwarg = {'password':{'write_only':True}, 'password':{'required': True}, 'email':{'required': True}, 'firstName':{'required': True}, 'lastName':{'required': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'], email=validated_data['email'], firstName=validated_data['firstName'], lastName=validated_data['lastName'])

        # add user to the UTrack_Users group
        user.groups.add(Group.objects.get(name='UTrack_Users'))
        return user