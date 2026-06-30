from django import forms
from django.core.exceptions import ValidationError
from .models import Loan


class LoanAdminForm(forms.ModelForm):

    class Meta:
        model = Loan
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        farmer = cleaned_data.get("farmer")

        if farmer and not self.instance.pk:  # only new loans
            active_loans = Loan.objects.filter(
                farmer=farmer
            ).exclude(
                status__in=["Completed", "Rejected"]
            )

            if active_loans.exists():
                raise ValidationError(
                    "This farmer already has an active loan. "
                    "Complete or reject the existing loan first."
                )

        return cleaned_data