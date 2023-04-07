from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

# Create your models here.
# Models are the database objects


class User(models.Model):
    username = models.CharField(max_length=8, primary_key=True)
    email = models.EmailField()
    firstName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=40)
    password = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.username}; {self.email}; {self.firstName}; {self.lastName}; {self.password}"


class Attendant(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Verifier(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Coach(models.Model):
    username = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    dinos_team = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username}; {self.dinos_team}"


class Tracked(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_hours = models.DecimalField(max_digits=7, decimal_places=2)
    
    def __str__(self):
        return f"{self.username}; {self.goal_hours}"


class HoursReport(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.username}; {self.hours}"


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
    facility_id = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.facility_id


class TrackedSessions(models.Model):
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    # attendant_username = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    facility = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=datetime.now)
    check_out_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.tracked_username}; {self.facility}; {self.check_in_time}; {self.check_out_time}"


class Alumnus(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Student(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class DinosMember(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    dinos_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username}; {self.dinos_team}"

class WorksAt(models.Model):
    username = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}; {self.facility_id}"


class FacilityUsage(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}; {self.facility_id}"


class ChecksIn(models.Model):
    attendant_username = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attendant_username}; {self.tracked_username}"


class LooksAt(models.Model):
    verifier_username = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    tracked_username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    hours = models.ForeignKey(HoursReport, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.verifier_username}; {self.tracked_username}; {self.hours}"


class Intramurals(models.Model):
    intramural_id = models.CharField(max_length=30, primary_key=True)
    intramural_team = models.CharField(max_length=50)
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.intramural_id}; {self.intramural_team}; {self.facility_id}"


class Class(models.Model):
    class_id = models.CharField(max_length=30, primary_key=True)
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_id}; {self.facility_id}"


class EnrolledIn(models.Model):
    username = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    no_of_classes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.username}; {self.class_id}; {self.no_of_classes}"


def validatePositive(value):
    if value < 0:
        raise ValidationError('Value must be positive.')


class EquipmentRentals(models.Model):
    facility_id = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cost = models.FloatField(validators=[validatePositive])

    def __str__(self):
        return f"{self.facility_id}; {self.name}; {self.cost}"


class CompetesIn(models.Model):
    tracked = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    intramural_id = models.ForeignKey(Intramurals, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tracked}; {self.intramural_id}"

