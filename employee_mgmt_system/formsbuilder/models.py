from django.db import models

# Create your models here.
from django.db import models

class DynamicForm(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FormField(models.Model):
    FIELD_TYPES = [
        ('text','Text'),
        ('number','Number'),
        ('date','Date'),
        ('password','Password'),
        ('textarea','Textarea'),
        ('email','Email'),
    ]
    form = models.ForeignKey(DynamicForm, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    key = models.CharField(max_length=200)  # e.g. "employee_name"
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.field_type})"
