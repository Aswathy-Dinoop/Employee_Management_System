from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeSerializer
from formsbuilder.models import DynamicForm, FormField
from formsbuilder.serializers import DynamicFormSerializer, FormFieldSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-created_at')
    serializer_class = EmployeeSerializer
    from rest_framework.permissions import IsAdminUser
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['data']

    def get_queryset(self):
        queryset = super().get_queryset()
        form_id = self.request.query_params.get('form_id')
        if form_id:
            queryset = queryset.filter(form_id=form_id)
        return queryset

class DynamicFormViewSet(viewsets.ModelViewSet):
    queryset = DynamicForm.objects.all().order_by('-created_at')
    serializer_class = DynamicFormSerializer
    permission_classes = [IsAuthenticated]

class FormFieldViewSet(viewsets.ModelViewSet):
    queryset = FormField.objects.all().order_by('order')
    serializer_class = FormFieldSerializer
    permission_classes = [IsAuthenticated]
