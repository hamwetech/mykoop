from django.urls import path
from . import views

urlpatterns = [
    path("loans/<int:pk>/", views.loan_detail, name="loan-detail"),
]