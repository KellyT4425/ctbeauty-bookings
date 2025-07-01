from . import views
from django.urls import path, include

app_name = "services"

urlpatterns = [
    path("", views.treatment_list, name="treatment_list"),

    # e.g. “/services/haircut/” shows the “haircut” treatment detail
    path("<slug:slug>/", views.treatment_detail, name="treatment_detail"),

]
