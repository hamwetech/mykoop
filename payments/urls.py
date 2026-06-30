from django.urls import path
from payments.views import (
    BulkPaymentUploadView,
    BulkPaymentConfirmView,
    BulkPaymentResultView
)

urlpatterns = [
    path("bulk/upload/", BulkPaymentUploadView.as_view(), name="bulk-upload"),
    path("bulk/confirm/", BulkPaymentConfirmView.as_view(), name="bulk-confirm"),
    path("bulk/result/<int:pk>/", BulkPaymentResultView.as_view(), name="bulk-payment-result"),
]