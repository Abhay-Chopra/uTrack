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
    time_in_facility = serializers.SerializerMethodField(method_name='calculate_time')
    
    class Meta:
        model = TrackedSessions
        fields = ['tracked_username', 'facility_id', 'check_in_time', 'check_out_time', 'time_in_facility']

    def calculate_time(self, instance):
        if instance.check_in_time != None and instance.check_out_time != None:
            time_elapsed =  instance.check_out_time - instance.check_in_time
            # Getting the hours and minutes of the elapsed time
            hours, remainder = divmod(time_elapsed.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours} hours, {minutes} minutes"
        return None

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
        fields = ['facility_id', 'facility_name']


class WorksAtSerializer(serializers.ModelSerializer):
    username = AttendantSerializer()
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = WorksAt
        fields = ['username', 'facility_id']


class UsesFacilitySerializer(serializers.ModelSerializer):
    tracked_username = TrackedSerializer()
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = UsesFacility
        fields = ['tracked_username', 'facility_id']


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


class IntramuralSerializer(serializers.ModelSerializer):
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = Intramural
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
        fields = ['username', 'class_id']


class EquipmentSerializer(serializers.ModelSerializer):
    facility_id = ActiveLivingFacilitySerializer()
    class Meta:
        model = Equipment
        fields = ['equipment_id', 'facility_id', 'description', 'cost']


class RentsEquipmentSerializer(serializers.ModelSerializer):
    username = UserSerializer
    class Meta:
        model = RentsEquipment
        fields = ['username', 'equipment_id']


class CompetesInSerializer(serializers.ModelSerializer):
    tracked = TrackedSerializer()
    intramural_id = IntramuralSerializer()
    class Meta:
        model = CompetesIn
        fields = ['tracked', 'intramural_id']


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
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        
        user.set_password(password)
        user.save()
        # adding user to a user group
        group = Group.objects.get(name=validated_data.pop('group'))
        user.groups.add(group)
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=24, write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if not user:
            raise ValidationError("Invalid login credentials")
        if not user.is_active:
            raise ValidationError("Inactive User")

        return user

