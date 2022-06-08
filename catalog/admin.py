from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import (
    User, ColumnType, Column, Schema, ColumnSeparator, Dataset
)


admin.site.register(User, UserAdmin)
admin.site.register(ColumnSeparator)
admin.site.register(Schema)
admin.site.register(ColumnType)
admin.site.register(Column)
admin.site.register(Dataset)
