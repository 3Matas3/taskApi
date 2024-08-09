from django.urls import path

from taskApi.api.views import DetailView, ModelListView, import_data

app_name = "api"

urlpatterns = [
    path("import", import_data, name="import_data"),
    path("detail/<str:model_name>", ModelListView.as_view(), name="detail_model"),
    path("detail/<str:model_name>/<int:pk>/", DetailView.as_view(), name="detail-view"),
]
