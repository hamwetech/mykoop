from django.contrib import admin
from .models import ExternalTrainer, TrainingSession, TrainingAttendance, ThematicArea


# -------------------------
# Thematic Area Admin
# -------------------------
@admin.register(ThematicArea)
class ThematicAreaAdmin(admin.ModelAdmin):
    list_display = ("thematic_area", "created_at", "updated_at")
    search_fields = ("thematic_area", "description")
    list_per_page = 20


# -------------------------
# External Trainer Admin
# -------------------------
@admin.register(ExternalTrainer)
class ExternalTrainerAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_per_page = 20


# -------------------------
# Training Attendance Inline
# -------------------------
class TrainingAttendanceInline(admin.TabularInline):
    model = TrainingAttendance
    extra = 1
    readonly_fields = ('training_reference',)
    fields = ('farmer', 'trainer', 'training_reference')
    show_change_link = True


# -------------------------
# Training Session Admin
# -------------------------
@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = (
        "training_reference",
        "topic",
        "trainer_name",
        "external_trainer_name",
        "is_external",
        "thematic_area",
        "training_start",
        "training_end",
        "duration_display",
    )
    list_filter = (
        "is_external",
        "thematic_area",
        "trainer",
        "external_trainer",
        "training_start",
    )
    search_fields = ("training_reference", "topic", "trainer__username", "external_trainer__name")
    inlines = [TrainingAttendanceInline]
    readonly_fields = ("duration_display",)

    def trainer_name(self, obj):
        return obj.trainer.get_full_name() if obj.trainer else "-"
    trainer_name.short_description = "Trainer"

    def external_trainer_name(self, obj):
        return obj.external_trainer.name if obj.external_trainer else "-"
    external_trainer_name.short_description = "External Trainer"

    def duration_display(self, obj):
        duration = obj.duration
        if duration:
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m"
        return "-"
    duration_display.short_description = "Duration"


# -------------------------
# Training Attendance Admin (Optional)
# -------------------------
@admin.register(TrainingAttendance)
class TrainingAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "training_reference_display",
        "farmer",
        "trainer",
    )
    list_filter = (
        "trainer",
        "training_session__thematic_area",
    )
    search_fields = (
        "training_reference",
        "farmer__surname",
        "farmer__first_name",
        "trainer__username",
    )

    def training_reference_display(self, obj):
        return obj.training_session.training_reference if obj.training_session else obj.training_reference
    training_reference_display.short_description = "Training Reference"
