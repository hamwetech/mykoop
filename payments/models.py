from django.db import models

from system.models import Farmer
from system.models import TimeStampMixin


class Transaction(TimeStampMixin):
    class CategoryOptions(models.TextChoices):
        COLLECTION = 'COLLECTION', 'COLLECTION'
        ORDER = 'ORDER', 'ORDER'
        SAVINGS = 'SAVINGS', 'SAVINGS'
        PAYOUT = 'PAYOUT', 'PAYOUT'

    farmer = models.ForeignKey(Farmer, null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_reference = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "transaction"



class Payment(TimeStampMixin):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
    ]

    farmer = models.ForeignKey(Farmer, null=True, blank=True, on_delete=models.CASCADE)
    reference = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    external_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "payment"


class PaymentBatch(TimeStampMixin):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed"),
    ]

    file = models.FileField(upload_to="bulk_payments/")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    total_records = models.IntegerField(default=0)
    successful = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)

    class Meta:
        db_table = "payment_batch"
    


class PaymentItem(models.Model):
    batch = models.ForeignKey(PaymentBatch, on_delete=models.CASCADE, related_name="items")

    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=50)

    status = models.CharField(
        max_length=20,
        choices=Payment.STATUS_CHOICES,
        default=Payment.PENDING
    )

    payment = models.OneToOneField(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "payment_item"


class PaymentLog(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    request_payload = models.TextField()
    response_payload = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment_log"
