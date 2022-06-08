from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser):
    pass


class ColumnSeparator(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"Column separator ({self.name})"


class Schema(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schema"
    )
    separator = models.ForeignKey(
        ColumnSeparator,
        on_delete=models.CASCADE,
        related_name="schema",
        null=False,
        blank=False
    )

    def get_absolute_url(self):
        return reverse("catalog:schema-detail", args=[str(self.id)])

    def get_all_columns(self):
        return self.column.all()

    def get_all_datasets(self):
        return self.dataset.all()

    def __str__(self):
        return self.name


class ColumnType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    order = models.IntegerField(null=False, blank=False, default=0)
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name="column"
    )
    type = models.ForeignKey(
        ColumnType,
        on_delete=models.CASCADE,
        related_name="column",
        null=False,
        blank=False
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Dataset(models.Model):
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name="dataset"
    )
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=255, null=False, blank=False)
    csv_file = models.FileField(upload_to="", null=True)
