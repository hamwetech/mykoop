from django.db import models
import datetime

from system.models import TimeStampMixin
from django.contrib.auth.models import User


class ThematicArea(TimeStampMixin):
    thematic_area = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)


    class Meta:
        db_table = 'thematic_area'

    def __str__(self):
        return self.thematic_area


class ExternalTrainer(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "external_trainer"
        verbose_name = "External Trainer"
        verbose_name_plural = "External Trainers"

    def __str__(self):
        return self.name


class TrainingSession(TimeStampMixin):
    thematic_area = models.ForeignKey(
        ThematicArea,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="training_sessions"
    )
    training_reference = models.CharField(max_length=256, null=True, blank=True, unique=True)
    trainer = models.ForeignKey(
        User,
        related_name='internal_trainings',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_external = models.BooleanField(default=False)
    external_trainer = models.ForeignKey(
        ExternalTrainer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="training_sessions"
    )
    topic = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gps_location = models.CharField(max_length=256, null=True, blank=True)
    training_start = models.DateTimeField()
    training_end = models.DateTimeField()
    training_image = models.ImageField(upload_to='training', null=True, blank=True)
    attendance_list_file = models.FileField(upload_to='trainingfiles', null=True, blank=True)


    class Meta:
        db_table = 'training_session'
        verbose_name = "Training Session"
        verbose_name_plural = "Training Sessions"
        ordering = ['-training_start']

    def __str__(self):
        return self.training_reference or f"{self.topic} ({self.training_start.date()})"

    @property
    def duration(self):
        """Return duration as timedelta if start and end exist."""
        if self.training_start and self.training_end:
            return self.training_end - self.training_start
        return None


class TrainingAttendance(TimeStampMixin):
    training_session = models.ForeignKey(
        TrainingSession,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    farmer = models.ForeignKey(
        'system.Farmer',
        on_delete=models.CASCADE,
        related_name="training_attendances"
    )
    trainer = models.ForeignKey(
        User,
        related_name='training_attendances',
        on_delete=models.CASCADE
    )
    # Optional: store a reference for offline/manual tracking
    training_reference = models.CharField(max_length=256, null=True, blank=True)
    is_synced = models.BooleanField(default=False)

    class Meta:
        db_table = 'training_attendance'
        verbose_name = "Training Attendance"
        verbose_name_plural = "Training Attendances"
        unique_together = ('training_session', 'farmer')  # prevent duplicate attendance

    def __str__(self):
        return f"{self.farmer} - {self.training_session}"