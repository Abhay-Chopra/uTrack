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

    def __str__(self):
        return f"{self.UCID}; {self.Ucalgary_email}; {self.Fname}; {self.Lname}; {self.Password}"


class Attendant(models.Model):
    UCID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.UCID


class Verifier(models.Model):
    UCID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.UCID

class Coach(models.Model):
    UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Dinos_team = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.UCID}; {self.Dinos_team}"


class Tracked(models.Model):
    UCID = models.ForeignKey(User, on_delete=models.CASCADE)
    Goal_hours = models.DecimalField(max_digits=7, decimal_places=2)
    
    def __str__(self):
        return f"{self.UCID}; {self.Goal_hours}"


class HoursReport(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Hours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.UCID}; {self.Hours}"


class ApplicationReviewer(models.Model):
    Verifier_UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Hours = models.ForeignKey(HoursReport, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Verifier_UCID}; {self.Tracked_UCID}; {self.Hours}"


class Oversees(models.Model):
    Verifier_UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.Verifier_UCID}; {self.Tracked_UCID}"


class TrackedSessions(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Facility = models.CharField(max_length=50)
    Check_in_time = models.DateTimeField(editable=False)
    Check_out_time = models.DateTimeField(editable=False)

    def __str__(self):
        return f"{self.UCID}; {self.Facility}; {self.Check_in_time}; {self.Check_out_time}"


class Alumnus(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return self.UCID


class Student(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return self.UCID


class DinosMember(models.Model):
    UCID = models.ForeignKey(Student, on_delete=models.CASCADE)
    Dinos_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.UCID}; {self.Dinos_team}"


class ActiveLivingFacility(models.Model):
    Facility_ID = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.Facility_ID


class WorksAt(models.Model):
    UCID = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.UCID}; {self.Facility_ID}"


class FacilityUsage(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.UCID}; {self.Facility_ID}"


class ChecksIn(models.Model):
    Attendant_UCID = models.ForeignKey(Attendant, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Attendant_UCID}; {self.Tracked_UCID}"


class LooksAt(models.Model):
    Verifier_UCID = models.ForeignKey(Verifier, on_delete=models.CASCADE)
    Tracked_UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Hours = models.ForeignKey(HoursReport, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Verifier_UCID}; {self.Tracked_UCID}; {self.Hours}"


class Intramurals(models.Model):
    Intramural_ID = models.CharField(max_length=30, primary_key=True)
    Intramural_team = models.CharField(max_length=50)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Intramural_ID}; {self.Intramural_team}; {self.Facility_ID}"


class Class(models.Model):
    Class_ID = models.CharField(max_length=30, primary_key=True)
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Class_ID}; {self.Facility_ID}"


class EnrolledIn(models.Model):
    UCID = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Class_ID = models.ForeignKey(Class, on_delete=models.CASCADE)
    No_of_classes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.UCID}; {self.Class_ID}; {self.No_of_classes}"


def validatePositive(value):
    if value < 0:
        raise ValidationError('Value must be positive.')


class EquipmentRentals(models.Model):
    Facility_ID = models.ForeignKey(ActiveLivingFacility, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Cost = models.FloatField(validators=[validatePositive])

    def __str__(self):
        return f"{self.Facility_ID}; {self.Name}; {self.Cost}"


class CompetesIn(models.Model):
    TRACKED = models.ForeignKey(Tracked, on_delete=models.CASCADE)
    Intramural_ID = models.ForeignKey(Intramurals, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.TRACKED}; {self.Intramural_ID}"

