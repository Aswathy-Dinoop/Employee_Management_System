from django.db import models
from django.conf import settings
from formsbuilder.models import DynamicForm

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    form = models.ForeignKey(DynamicForm, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField(default=dict, blank=True, null=True)  # to store answers from dynamic form
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Employee {self.id}"