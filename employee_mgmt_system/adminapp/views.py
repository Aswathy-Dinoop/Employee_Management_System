from django.shortcuts import render
from django.contrib.auth.models import User

from ems_app.models import Employee

from django.shortcuts import render, get_object_or_404, redirect
from formsbuilder.models import DynamicForm, FormField

# Create your views here.
def admin_dashboard(request):
    return render(request, 'admin/admin_index.html')

def view_employees(request):
    from django.db.models import Q
    employees = Employee.objects.select_related('user').all()
    q = request.GET.get('q', '').strip()
    if q:
        employees = employees.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(user__email__icontains=q)
        )
    # Dynamic field filters
    if employees and employees.first() and employees.first().form:
        for field in employees.first().form.fields.all():
            filter_val = request.GET.get(f'filter_{field.key}', '').strip()
            if filter_val:
                employees = employees.filter(**{f'data__{field.key}__icontains': filter_val})
    return render(request, 'admin/view_employee.html', {'employees': employees})

def employee_create(request):
    forms = DynamicForm.objects.all()
    fields = []
    selected_form = None
    error = None
    if request.method == "POST":
        form_id = request.POST.get("form_id")
        selected_form = get_object_or_404(DynamicForm, pk=form_id) if form_id else None
        data = {}
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        email2 = request.POST.get("email2")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if selected_form:
            # Only require confirmation if present
            if password2 and password != password2:
                error = "Passwords do not match."
            elif email2 and email != email2:
                error = "Emails do not match."
            elif User.objects.filter(username=username).exists():
                error = "Username already exists. Please choose another."
            else:
                for field in selected_form.fields.all():
                    field_value = request.POST.get(field.key, "")
                    data[field.key] = field_value
                    # If the dynamic form has a password/email field, compare to login field
                    if field.key == "password" and field_value and field_value != password:
                        error = "Password in form field does not match login password."
                    if field.key == "email" and field_value and field_value != email:
                        error = "Email in form field does not match login email."
                if error:
                    fields = selected_form.fields.all() if selected_form else []
                else:
                    try:
                        user = User.objects.create_user(
                            username=username,
                            password=password,
                            email=email,
                            first_name=first_name,
                            last_name=last_name
                        )
                        employee = Employee.objects.create(user=user, form=selected_form, data=data)
                        return redirect("view_employees")
                    except Exception as e:
                        error = str(e)
                fields = selected_form.fields.all() if selected_form else []
    return render(request, "admin/employee_create.html", {
        "forms": forms,
        "fields": fields,
        "selected_form": selected_form,
        "error": error,
    })

from formsbuilder.models import DynamicForm  # import at top

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    error = None

    if request.method == "POST":
        form_id = request.POST.get("form_id")
        if form_id:
            employee.form = get_object_or_404(DynamicForm, pk=form_id)

        data = {}
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        email2 = request.POST.get("email2")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Only require confirmation if present
        if password2 and password != password2:
            error = "Passwords do not match."
        elif email2 and email != email2:
            error = "Emails do not match."
        else:
            if employee.form:
                for field in employee.form.fields.all():
                    field_value = request.POST.get(field.key, "")
                    data[field.key] = field_value
                    # If the dynamic form has a password/email field, compare to login field
                    if field.key == "password" and field_value and field_value != password:
                        error = "Password in form field does not match login password."
                    if field.key == "email" and field_value and field_value != email:
                        error = "Email in form field does not match login email."
            if not error:
                employee.data = data
                # Update linked User model
                user = employee.user
                if user:
                    if password:
                        user.set_password(password)
                    if email:
                        user.email = email
                    if first_name:
                        user.first_name = first_name
                    if last_name:
                        user.last_name = last_name
                    user.save()
                employee.save()
                return redirect("view_employees")

    forms = DynamicForm.objects.all()
    fields = employee.form.fields.all() if employee.form else []

    return render(request, "admin/employee_edit.html", {
        "employee": employee,
        "forms": forms,
        "fields": fields,
        "error": error,
    })

def employee_delete(request, pk):
    from ems_app.models import Employee
    from django.contrib.auth.models import User
    employee = get_object_or_404(Employee, pk=pk)
    user = employee.user
    employee.delete()
    if user:
        # Double check and delete user if still exists
        try:
            user.delete()
        except User.DoesNotExist:
            pass
    return redirect("view_employees")