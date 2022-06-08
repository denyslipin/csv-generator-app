from django.urls import path

from catalog.views import (
    index,
    schema_list_view,
    schema_detail_view,
    schema_create_view,
    schema_update_view,
    schema_delete_view
)

urlpatterns = [
    path("", index, name="index"),
    path("schemas/", schema_list_view, name="schema-list"),
    path("schemas/<int:pk>/", schema_detail_view, name="schema-detail"),
    path("schemas/create/", schema_create_view, name="schema-create"),
    path("schemas/<int:pk>/update/", schema_update_view, name="schema-update"),
    path("schemas/<int:pk>/delete/", schema_delete_view, name="schema-delete"),
]

app_name = "catalog"
