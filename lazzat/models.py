from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Staff(models.Model):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField()

    def __str__(self):
        return self.first_name

class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name

class StaffShift(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('staff', 'date')

    def __str__(self):
        return self.staff.first_name + self.shift.name

class StaffAttendance(models.Model):
    staff_shift = models.OneToOneField(StaffShift, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ])

    def __str__(self):  
        return f"{self.staff_shift.staff} - {self.staff_shift.date} - {self.status}"
