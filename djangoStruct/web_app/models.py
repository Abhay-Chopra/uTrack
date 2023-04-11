from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
# Models are the database objects


class Attendant(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')

    def __str__(self):
        return self.username


class Verifier(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')

    def __str__(self):
        return self.username


class Coach(models.Model):
    username = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    dinos_team = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username}; {self.dinos_team}"


class Tracked(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    goal_hours = models.DecimalField(max_digits=7, decimal_places=2)
    
    def __str__(self):
        return f"{self.username}; {self.goal_hours}"

###### DO THIS ######
class HoursReport(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.username}; {self.hours}"

###### DO THIS ######
class ApplicationReviewer(models.Model):
    verifier_username = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    hours = models.ForeignKey(HoursReport, on_delete=models.CASCADE)  # I think this references 'username' in HoursReport

    def __str__(self):
        return f"{self.verifier_username}; {self.tracked_username}; {self.hours}"


# We can forgo this relation as its just easier to have the attendant directly on the tracked sessions
class Oversees(models.Model):
    verifier_username = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.verifier_username}; {self.tracked_username}"


class ActiveLivingFacility(models.Model):
    facility_id = models.IntegerField(primary_key=True, validators=[MaxValueValidator(15)])
    facility_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.facility_id}; {self.facility_name}"


class TrackedSessions(models.Model):
    tracked_username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    # TODO Make this a foreign key to Active Living Facility when that table has been populated
    facility_id = models.IntegerField()
    check_in_time = models.DateTimeField(default=datetime.now)
    check_out_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.tracked_username}; {self.facility_id}; {self.check_in_time}; {self.check_out_time}"


class Alumnus(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Student(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


###### DO THIS ######
class DinosMember(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    dinos_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username}; {self.dinos_team}"


###### DO THIS ######
class WorksAt(models.Model):
    attendant_username = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attendant_username}; {self.facility_id}"


class UsesFacility(models.Model):
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tracked_username}; {self.facility_id}"


class ChecksIn(models.Model):
    attendant_username = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attendant_username}; {self.tracked_username}"


###### DO THIS ######
class LooksAt(models.Model):
    verifier_username = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    hours = models.ForeignKey(HoursReport, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.verifier_username}; {self.tracked_username}; {self.hours}"


class Intramural(models.Model):
    intramural_id = models.IntegerField(primary_key=True, validators=[MaxValueValidator(15)])
    intramural_name = models.CharField(max_length=50, unique=True)
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.intramural_id}; {self.intramural_name}; {self.facility_id}"


class Class(models.Model):
    class_id = models.IntegerField(primary_key=True, validators=[MaxValueValidator(15)])
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_id}; {self.facility_id}"


class EnrolledIn(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}; {self.class_id}"


def validatePositive(value):
    if value < 0:
        raise ValidationError('Value must be positive.')


class Equipment(models.Model):
    equipment_id = models.IntegerField(primary_key=True, validators=[MaxValueValidator(15)])
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    cost = models.FloatField(validators=[validatePositive])

    def __str__(self):
        return f"{self.equipment_id}; {self.facility_id}; {self.description}; {self.cost}"


# Assuming coaches and verifiers can rent equipment (using username instead of tracked)
class RentsEquipment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    equipment_id = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}; {self.equipment_id}"


class CompetesIn(models.Model):
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    intramural_id = models.ForeignKey(Intramural, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tracked_username}; {self.intramural_id}"

