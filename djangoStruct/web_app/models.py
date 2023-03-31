from django.core.exceptions import ValidationError
from django.db import models
  
# Create your models here.
# Models are the database objects


class React(models.Model):
    name = models.CharField(max_length=30)
    detail = models.CharField(max_length=500)



class User(models.Model):
    UCID = models.CharField(max_length=8, primary_key=True)
    Ucalgary_email = models.EmailField()
    Fname = models.CharField(max_length=50)
    Lname = models.CharField(max_length=50)
    Password = models.CharField(max_length=25)


class Attendant(models.Model):
    UCID = models.ForeignKey(User, on_delete=models.CASCADE)


class Verifier(models.Model):
    UCID = models.ForeignKey(User, on_delete=models.CASCADE)


class Coach(models.Model):
    UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Dinos_team = models.CharField(max_length=50)


class Tracked(models.Model):
    UCID = models.ForeignKey(User, on_delete=models.CASCADE)
    Goal_hours = models.DecimalField(max_digits=7, decimal_places=2)


class HoursReport(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Hours = models.DecimalField(max_digits=5, decimal_places=2)


class ApplicationReviewer(models.Model):
    Verifier_UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Hours = models.ForeignKey(HoursReport, on_delete=models.CASCADE)


class Oversees(models.Model):
    Verifier_UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)


class TrackedSessions(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Facility = models.CharField(max_length=50)
    Check_in_time = models.DateTimeField(editable=False)
    Check_out_time = models.DateTimeField(editable=False)


class Alumnus(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)


class Student(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)


class DinosMember(models.Model):
    UCID = models.ForeignKey(Student, on_delete=models.CASCADE)
    Dinos_team = models.CharField(max_length=100)


class ActiveLivingFacility(models.Model):
    Facility_ID = models.CharField(max_length=20, primary_key=True)


class WorksAt(models.Model):
    UCID = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)


class FacilityUsage(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)


class ChecksIn(models.Model):
    Attendant_UCID = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)


class LooksAt(models.Model):
    Verifier_UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Hours = models.ForeignKey(HoursReport, on_delete=models.CASCADE)


class Intramurals(models.Model):
    Intramural_ID = models.CharField(max_length=30, primary_key=True)
    Intramural_team = models.CharField(max_length=50)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)


class Class(models.Model):
    Class_ID = models.CharField(max_length=30, primary_key=True)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)


class EnrolledIn(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Class_ID = models.ForeignKey(Class, on_delete=models.CASCADE)
    No_of_classes = models.PositiveIntegerField()


def validatePositive(value):
    if value < 0:
        raise ValidationError('Value must be positive.')


class EquipmentRentals(models.Model):
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Cost = models.FloatField(validators=[validatePositive])


class CompetesIn(models.Model):
    TRACKED = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Intramural_ID = models.ForeignKey(Intramurals, on_delete=models.CASCADE)

