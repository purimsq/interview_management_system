from django.db import models
from django.contrib.auth.models import AbstractUser


# User model with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('superadmin', 'Super Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_suspended = models.BooleanField(default=False)

# SuspendedStudent model
class SuspendedStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    suspension_reason = models.TextField()

# Request model
class Request(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    request_text = models.TextField()
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending')

# Report model for teachers
class Report(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_text = models.TextField()

# Login history model
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    changes_made = models.TextField()

    class Enquiry(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    current_class = models.CharField(max_length=10)
    admission_class = models.CharField(max_length=10)
    residence_zone = models.CharField(max_length=100)
    current_school = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    alternative_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    has_siblings = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.admission_class}"