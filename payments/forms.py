from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from payments.models import PaymentBatch

class BulkPaymentUploadForm(forms.ModelForm):
    class Meta:
        model = PaymentBatch
        fields = ["file"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False