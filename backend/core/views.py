from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import User, Student, SuspendedStudent, Request, Report, LoginHistory
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Enquiry
from .serializers import EnquirySerializer

# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = User.objects.create_user(username=username, password=password, role=role)
        if role == 'student':
            Student.objects.create(user=user)
        return redirect('login')
    return render(request, 'register.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

# Admin dashboard view
@login_required
@user_passes_test(lambda u: u.role == 'admin')
def admin_dashboard(request):
    students = Student.objects.all()
    suspended_students = SuspendedStudent.objects.all()
    pending_requests = Request.objects.filter(status='pending')
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')
        student = Student.objects.get(id=student_id)
        if action == 'suspend':
            SuspendedStudent.objects.create(student=student)
            student.is_suspended = True
        elif action == 'unsuspend':
            SuspendedStudent.objects.filter(student=student).delete()
            student.is_suspended = False
        student.save()
    return render(request, 'admin_dashboard.html', {
        'students': students,
        'suspended_students': suspended_students,
        'pending_requests': pending_requests,
    })

# Teacher dashboard view
@login_required
@user_passes_test(lambda u: u.role == 'teacher')
def teacher_dashboard(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        report_text = request.POST['report_text']
        student = Student.objects.get(id=student_id)
        Report.objects.create(teacher=request.user, student=student, report_text=report_text)
    return render(request, 'teacher_dashboard.html', {'students': Student.objects.all()})

# Super admin dashboard view
@login_required
@user_passes_test(lambda u: u.role == 'superadmin')
def superadmin_dashboard(request):
    login_history = LoginHistory.objects.all()
    return render(request, 'superadmin_dashboard.html', {'login_history': login_history})

@api_view(['POST'])
def submit_enquiry(request):
    serializer = EnquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)