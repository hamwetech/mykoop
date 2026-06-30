from django.db import models

from system.models import TimeStampMixin


class SmsLog(TimeStampMixin):
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20)  # e.g., SUCCESS, FAILED, PENDING
    api_response = models.JSONField(null=True, blank=True)  # store JSON response
    error = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.recipient} - {self.status} - {self.created_at}"
