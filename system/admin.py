from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from django.shortcuts import render, get_object_or_404

from system.models import Collection
from system.models.application import DeviceHeartBeat
from .forms import FarmerAdminForm
from .models import Farmer, Clan, Cooperative, FarmerGroup, AppVersion, Attendance, Meeting


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'member_id', 'clan', 'gender', 'date_of_birth', 'district', 'county', 'created_at', 'open_button')
    search_fields = ('get_name', 'clan', 'gender')
    list_filter  = ('gender', 'clan', 'district')

    fieldsets = (

        ("Personal Information", {
            "fields": (
                "image",
                "title",
                "surname",
                "first_name",
                "other_name",
                "gender",
                "date_of_birth",
                "marital_status",
                "children_number",
                "education_level",
                "profession",
                "cooperative",
                "farmer_group",
                "is_refugee",
                "is_handicap",
            )
        }),

        ("Identification", {
            "fields": (
                "id_type",
                "id_number",
                "card_number",
                "qrcode",
            )
        }),

        ("Contact Information", {
            "fields": (
                "phone_number",
                "other_phone_number",
                "own_phone",
                "has_mobile_money",
                "email",
            )
        }),

        ("Location", {
            "fields": (
                "land_acreage",
                "land_ownership",
                "district",
                "county",
                "sub_county",
                "parish",
                "village",
                "address",
                "gps_coordinates",
            ),
            "classes": ("collapse",)
        }),

        ("Products / Activities", {
            "fields": (
                "crop",
            )
        }),

        ("Financial Information", {
            "fields": (
                "savings_balance",
                "shares_balance",
                "account_balance",
                "create_wallet",
                "has_flexipay",
            )
        }),

        ("System Information", {
            "fields": (
                "is_active",
                "created_by",
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",)
        }),
    )

    readonly_fields = (
        "member_id",
        "created_at",
        "updated_at",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'detail/<int:farmer_id>/',
                self.admin_site.admin_view(self.farmer_detail),
                name='system_farmer'  # <- include app label and model name to avoid conflicts
            ),
        ]
        return custom_urls + urls

    def open_button(self, obj):
        url = reverse('admin:system_farmer', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}">Open</a>', url)

    open_button.short_description = 'Action'
    open_button.allow_tags = True  # optional in newer Django versions

    def farmer_detail(self, request, farmer_id):
        farmer = get_object_or_404(self.get_queryset(request), id=farmer_id)
        context = dict(
            self.admin_site.each_context(request),
            farmer=farmer
        )
        return render(request, "admin/system/farmer/farmer_detail.html", context)


@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'totem', 'farmer_count')
    search_fields = ('name',)


@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'district', 'county' ,'sub_county', 'farmer_count')
    search_fields = ('name',)


@admin.register(FarmerGroup)
class FarmerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooperative', 'district', 'county' ,'sub_county', 'farmer_count')
    search_fields = ('name',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):

    list_display = (
        "collection_reference",
        "collection_date",
        "farmer",
        "cooperative",
        "product",
        "quantity",
        "unit_price",
        "total_price",
        "repay_loan",
    )

    list_filter = (
        "collection_date",
        "cooperative",
        "product",
        "repay_loan",
    )

    search_fields = (
        "collection_reference",
        "name",
        "phone_number",
        "farmer__surname",
        "farmer__first_name",
    )

    exclude = ("name", "phone_number", "collection_reference")

    date_hierarchy = "collection_date"

    ordering = ("-collection_date",)

    # readonly_fields = ('unit_price', 'total_price')


@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ("version_name", "version_code", "force_update", "is_active")


@admin.register(DeviceHeartBeat)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ("device", "entry_date", "gps_coodinates")


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    fields = (
        "farmer",
        "status",
        "present",
        "remarks",
    )


# @admin.register(Meeting)
# class MeetingAdmin(admin.ModelAdmin):
#     list_display = (
#         "meeting_number",
#         "meeting_date",
#         "venue",
#         "chaired_by",
#         "secretary",
#         "status",
#     )

#     list_filter = (
#         "status",
#         "meeting_date",
#     )

#     search_fields = (
#         "meeting_number",
#         "venue",
#         "chaired_by__name",
#         "secretary__name",
#     )

#     inlines = [
#         AttendanceInline,
#     ]

#     date_hierarchy = "meeting_date"


# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = (
#         "meeting",
#         "farmer",
#         "status",
#         "present",
#         "created_at",
#     )

#     list_filter = (
#         "status",
#         "present",
#         "meeting",
#     )

#     search_fields = (
#         "farmer__name",
#         "meeting__meeting_number",
#     )


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    autocomplete_fields = ["farmer"]
    fields = ("farmer", "status", "present", "remarks")


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        "meeting_number",
        "meeting_date",
        "venue",
        "chaired_by",
        "secretary",
        "status",
        "attendance_count",
    )

    list_filter = (
        "status",
        "meeting_date",
        "chaired_by",
    )

    search_fields = (
        "meeting_number",
        "venue",
        "chaired_by__name",
        "secretary__name",
        "agenda",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "meeting_date"

    ordering = ("-meeting_date", "-meeting_number")

    autocomplete_fields = (
        "chaired_by",
        "secretary",
    )

    inlines = [AttendanceInline]

    fieldsets = (
        (
            "Meeting Details",
            {
                "fields": (
                    "meeting_number",
                    "meeting_date",
                    "venue",
                    "status",
                )
            },
        ),
        (
            "Leadership",
            {
                "fields": (
                    "chaired_by",
                    "secretary",
                )
            },
        ),
        (
            "Documentation",
            {
                "fields": (
                    "agenda",
                    "minutes",
                    "notes",
                )
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Attendance")
    def attendance_count(self, obj):
        present = obj.attendance_set.filter(status="Present").count()
        total = obj.attendance_set.count()
        return f"{present}/{total}"


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "meeting",
        "farmer",
        "status",
        "present",
        "remarks",
    )

    list_filter = (
        "status",
        "present",
        "meeting__meeting_date",
    )

    search_fields = (
        "farmer__name",
        "meeting__meeting_number",
        "remarks",
    )

    autocomplete_fields = (
        "meeting",
        "farmer",
    )

    ordering = (
        "-meeting__meeting_date",
        "farmer__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


