from django import forms
from django.forms.models import modelformset_factory

from catalog.models import Schema, Column


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "separator"]


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ["name", "type", "order"]


ColumnFormset = modelformset_factory(
    Column,
    form=ColumnForm,
    extra=0
)
