from django import forms

from conf.models import District
from system.models import Clan
from .models import SmsLog
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div


class SendSmsForm(forms.Form):

    MESSAGE_TYPE_CHOICES = [
        ("open", "Open"),
        ("farmerlist", "Farmer List"),
    ]

    GROUPING_CHOICES = [
        ("all", "All Farmers"),
        ("district", "By District"),
        ("clan", "By Clan"),
    ]

    message_type = forms.ChoiceField(
        choices=MESSAGE_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    grouping = forms.ChoiceField(
        choices=GROUPING_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control select2"})
    )

    district = forms.ModelMultipleChoiceField(
        queryset=District.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control select2"})
    )

    clan = forms.ModelMultipleChoiceField(
        queryset=Clan.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control select2"})
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )

    recipients = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 2,
            "placeholder": "e.g. 2567xxxxxxx,2567xxxxxxx"
        }),
    )

    schedule_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            "type": "datetime-local",
            "class": "form-control"
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False


    # 🔥 Validation
    def clean(self):
        cleaned_data = super().clean()

        message_type = cleaned_data.get("message_type")
        grouping = cleaned_data.get("grouping")
        recipients = cleaned_data.get("recipients")
        district = cleaned_data.get("district")
        clan = cleaned_data.get("clan")

        if message_type == "open" and not recipients:
            raise forms.ValidationError("Recipients are required for open messages.")

        if message_type == "farmerlist":
            if not grouping:
                raise forms.ValidationError("Grouping is required.")

            if grouping == "district" and not district:
                raise forms.ValidationError("Select a district.")

            if grouping == "clan" and not clan:
                raise forms.ValidationError("Select a clan.")

        return cleaned_data


class SmsLogAdminForm(forms.ModelForm):
    class Meta:
        model = SmsLog
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        # Optional: enforce rules (but mostly logs shouldn't be edited)
        return cleaned_data