from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    redirect, render, get_object_or_404, HttpResponseRedirect
)

from catalog.forms import SchemaForm, ColumnFormset
from catalog.models import Schema, Column, Dataset
from catalog.tasks import generate_csv


@login_required
def index(request):
    """View function for the home page of the site."""

    num_schemas = Schema.objects.count()
    num_columns = Column.objects.count()
    num_datasets = Dataset.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_schemas": num_schemas,
        "num_columns": num_columns,
        "num_datasets": num_datasets,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


@login_required
def schema_list_view(request):
    schema_list = Schema.objects.filter(user=request.user)
    context = {
        "schema_list": schema_list
    }
    return render(request, "catalog/schema_list.html", context=context)


@login_required
def schema_detail_view(request, pk=None):
    schema = get_object_or_404(Schema, pk=pk, user=request.user)
    context = {
        "schema": schema
    }
    if request.method == "POST":
        rows = int(request.POST["rows"])
        dataset = Dataset.objects.create(schema=schema, status="In progress")
        generate_csv.delay(rows, schema.id, dataset.id)
        return redirect(schema.get_absolute_url())
    return render(request, "catalog/schema_detail.html", context=context)


@login_required
def schema_create_view(request):
    form = SchemaForm(request.POST or None)
    formset = ColumnFormset(
        request.POST or None,
        queryset=Column.objects.none()
    )
    context = {
        "form": form,
        "formset": formset,
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.user = request.user
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.schema = parent
            child.save()
        return redirect(parent.get_absolute_url())
    return render(request, "catalog/schema_form.html", context=context)


@login_required
def schema_update_view(request, pk=None):
    schema = get_object_or_404(Schema, pk=pk, user=request.user)
    form = SchemaForm(request.POST or None, instance=schema)
    formset = ColumnFormset(
        request.POST or None,
        queryset=schema.get_all_columns()
    )
    context = {
        "form": form,
        "formset": formset,
        "schema": schema
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.schema = parent
            child.save()
        return redirect(schema.get_absolute_url())
    return render(request, "catalog/schema_form.html", context=context)


@login_required
def schema_delete_view(request, pk=None):
    schema = get_object_or_404(Schema, pk=pk, user=request.user)
    context = {
        "schema": schema
    }
    if request.method == "POST":
        schema.delete()
        return HttpResponseRedirect("/schemas")
    return render(
        request,
        "catalog/schema_confirm_delete.html",
        context=context
    )
