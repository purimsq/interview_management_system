from rest_framework import serializers
from .models import Enquiry
from .models import Student, Sibling, ParentGuardian, PendingRequest

class SiblingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sibling
        fields = ['name', 'grade', 'year_admitted']

class ParentGuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentGuardian
        fields = ['name', 'relationship', 'phone_number', 'email']

class StudentSerializer(serializers.ModelSerializer):
    siblings = SiblingSerializer(many=True, required=False)
    parents = ParentGuardianSerializer(many=True, required=False)

    class Meta:
        model = Student
        fields = '__all__'

class PendingRequestSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = PendingRequest
        fields = '__all__'

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'