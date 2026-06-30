from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'device'


class DeviceHeartBeat(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    gps_coodinates = models.CharField(max_length=120, null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    entry_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'device_heartbeat'


class AppVersion(models.Model):
    version_code = models.IntegerField(unique=True)
    version_name = models.CharField(max_length=20)
    apk_file = models.FileField(upload_to="apks/")
    is_active = models.BooleanField(default=True)
    force_update = models.BooleanField(default=False)
    release_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_version'

    def __str__(self):
        return self.version_name