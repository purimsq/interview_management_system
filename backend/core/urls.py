from django.urls import path
from .views import register, login_view, admin_dashboard, teacher_dashboard, superadmin_dashboard, submit_enquiry

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
    path('submit_enquiry/', submit_enquiry, name='submit_enquiry'),
]

