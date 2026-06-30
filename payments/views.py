from django.views.generic import FormView, DetailView
from django.shortcuts import render, redirect
from payments.forms import BulkPaymentUploadForm
from payments.utils import parse_bulk_payment_file
from payments.models import PaymentBatch
import requests
from django.views import View


class BulkPaymentUploadView(FormView):
    template_name = "payments/upload.html"
    form_class = BulkPaymentUploadForm

    def form_valid(self, form):
        batch = form.save(commit=False)
        batch.created_by = self.request.user
        batch.save()

        payments = parse_bulk_payment_file(batch.file)

        self.request.session["bulk_payments"] = payments
        self.request.session["batch_id"] = batch.id

        return render(self.request, "payments/confirm.html", {
            "payments": payments,
            "batch": batch
        })


class BulkPaymentConfirmView(View):

    def post(self, request):
        payments = request.session.get("bulk_payments", [])
        batch_id = request.session.get("batch_id")

        batch = PaymentBatch.objects.get(id=batch_id)

        batch.status = PaymentBatch.PROCESSING
        batch.total_records = len(payments)
        batch.save()

        success = 0
        failed = 0

        for p in payments:
            try:
                payload = {
                    "msisdn": p["phone"],
                    "amount": p["amount"],
                    "reference": p["reference"],
                }

                # Example API call (replace with real provider)
                response = requests.post("https://payment-api/send", json=payload)

                if response.status_code == 200:
                    success += 1
                else:
                    failed += 1

            except Exception:
                failed += 1

        batch.successful = success
        batch.failed = failed
        batch.status = PaymentBatch.COMPLETED
        batch.save()

        request.session.pop("bulk_payments", None)
        request.session.pop("batch_id", None)

        return redirect("bulk-payment-result", batch.id)
    

class BulkPaymentResultView(DetailView):
    model = PaymentBatch
    template_name = "payments/result.html"
    context_object_name = "batch"