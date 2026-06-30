# services/payments.py
import requests
import uuid
from django.conf import settings
from .models import Payment
from payments.models import PaymentBatch

class PaymentService:

    @staticmethod
    def initiate_payment(farmer, amount, phone):
        reference = f"BKK-{uuid.uuid4().hex[:10]}"

        payment = Payment.objects.create(
            farmer=farmer,
            amount=amount,
            phone_number=phone,
            reference=reference,
        )

        payload = {
            "amount": str(amount),
            "msisdn": phone,
            "reference": reference,
            "callback_url": settings.PAYMENT_CALLBACK_URL,
        }

        response = requests.post(settings.PAYMENT_URL, json=payload)

        data = response.json()

        payment.external_id = data.get("transaction_id")
        payment.save()

        return payment


class BulkPaymentProcessor:

    @staticmethod
    def process_batch(batch):
        items = batch.items.all()

        batch.status = PaymentBatch.PROCESSING
        batch.total_records = items.count()
        batch.save()

        success = 0
        failed = 0

        for item in items:
            payment = PaymentService.send_payment(
                phone=item.phone_number,
                amount=item.amount,
                batch=batch,
                reference=item.reference
            )

            item.payment = payment
            item.status = payment.status
            item.save()

            if payment.status == Payment.SUCCESS:
                success += 1
            else:
                failed += 1

        batch.successful = success
        batch.failed = failed
        batch.status = PaymentBatch.COMPLETED
        batch.save()