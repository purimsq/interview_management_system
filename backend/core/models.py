from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('superadmin', 'Super Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_groups', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )



class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_suspended = models.BooleanField(default=False)


class SuspendedStudent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    suspension_reason = models.TextField()


class Request(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    request_text = models.TextField()
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending')


class Report(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_text = models.TextField()


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    changes_made = models.TextField()

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    current_class = models.CharField(max_length=50)
    admission_class = models.CharField(max_length=50)
    residence_zone = models.CharField(max_length=100)
    current_school = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    alternative_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    has_siblings = models.BooleanField(default=False)

class Sibling(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='siblings')
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    year_admitted = models.IntegerField()

class ParentGuardian(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)  # Parent or Guardian
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

class PendingRequest(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"
    

class Enquiry(models.Model):
    pupil = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')])

    def __str__(self):
        return f"Enquiry for {self.pupil.first_name} {self.pupil.surname} - {self.status}"

