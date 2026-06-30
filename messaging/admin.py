from django import forms
from django.contrib import admin
from django.contrib import messages
from django.urls import path, reverse
from django.shortcuts import render, redirect

from messaging.forms import SendSmsForm
from messaging.models import SmsLog
from messaging.utils import send_sms
from system.models import Farmer


@admin.register(SmsLog)
class SmsLogAdmin(admin.ModelAdmin):
    list_display = ("recipient", "status", "sender", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("recipient", "message")
    readonly_fields = (
        "recipient",
        "message",
        "status",
        "api_response",
        "error",
        "sender",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-sms/",
                self.admin_site.admin_view(self.send_sms_view),
                name="messaging_smslog_send_sms",
            ),
        ]
        return custom_urls + urls

    def send_sms_view(self, request):
        form = SendSmsForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            data = form.cleaned_data

            message = data["message"]
            message_type = data["message_type"]

            recipients = []

            #1. OPEN (manual numbers)
            if message_type == "open":
                raw_numbers = data.get("recipients", "")
                recipients = [num.strip() for num in raw_numbers.split(",") if num.strip()]

            #2. FARMER LIST (filtered)
            elif message_type == "farmerlist":
                grouping = data.get("grouping")

                if grouping == "all":
                    recipients = Farmer.objects.values_list("phone_number", flat=True)

                elif grouping == "district":
                    districts = data.get("district")
                    recipients = Farmer.objects.filter(
                        district__in=districts
                    ).values_list("phone_number", flat=True)

                elif grouping == "clan":
                    clans = data.get("clan")
                    recipients = Farmer.objects.filter(
                        clan__in=clans
                    ).values_list("phone_number", flat=True)

            #Remove duplicates + empty numbers
            recipients = list(set([r for r in recipients if r]))

            #SEND SMS
            sent_count = 0
            for phone in recipients:
                try:
                    # 👉 your SMS function
                    send_sms(phone, message)
                    sent_count += 1
                except Exception as e:
                    # optional: log error
                    pass

            #Success message
            messages.success(request, f"SMS sent to {sent_count} recipients")

            return redirect("..")

        context = dict(
            self.admin_site.each_context(request),
            form=form,
        )
        return render(request, "admin/messaging/send_sms.html", context)
