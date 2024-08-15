from django.contrib import admin
from .models import Student, Sibling, ParentGuardian, PendingRequest

class SiblingInline(admin.TabularInline):
    model = Sibling
    extra = 1

class ParentGuardianInline(admin.TabularInline):
    model = ParentGuardian
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    inlines = [SiblingInline, ParentGuardianInline]

class PendingRequestAdmin(admin.ModelAdmin):
    model = PendingRequest

admin.site.register(Student, StudentAdmin)
admin.site.register(PendingRequest, PendingRequestAdmin)



