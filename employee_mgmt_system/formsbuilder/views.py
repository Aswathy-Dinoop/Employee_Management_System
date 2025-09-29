from django.shortcuts import render, redirect, get_object_or_404
from .models import DynamicForm, FormField

def form_list(request):
    forms = DynamicForm.objects.all()
    return render(request, "formsbuilder/form_list.html", {"forms": forms})

def form_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        form = DynamicForm.objects.create(name=name, description=description)
        return redirect("form_edit", pk=form.id)
    return render(request, "formsbuilder/form_create.html")

def form_edit(request, pk):
    form = get_object_or_404(DynamicForm, pk=pk)
    if request.method == "POST":
        label = request.POST.get("label")
        key = request.POST.get("key")
        field_type = request.POST.get("field_type")
        required = request.POST.get("required") == "on"
        order = request.POST.get("order") or 0
        FormField.objects.create(
            form=form, label=label, key=key,
            field_type=field_type, required=required, order=order
        )
        return redirect("form_edit", pk=form.id)

    return render(request, "formsbuilder/form_edit.html", {"form": form})

def form_delete(request, pk):
    form = get_object_or_404(DynamicForm, pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect("form_list")
    return redirect("form_list")
