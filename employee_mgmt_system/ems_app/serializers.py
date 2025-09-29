from rest_framework import serializers
from .models import Employee
from formsbuilder.models import DynamicForm, FormField

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'label', 'key', 'field_type', 'required', 'order']

class DynamicFormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)
    class Meta:
        model = DynamicForm
        fields = ['id', 'name', 'description', 'created_at', 'fields']

class EmployeeSerializer(serializers.ModelSerializer):
    form = DynamicFormSerializer(read_only=True)
    class Meta:
        model = Employee
        fields = ['id', 'form', 'data', 'created_at', 'updated_at']
