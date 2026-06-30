from email import message

from django.db.models.signals import post_save
from django.dispatch import receiver

from conf.utils import log_debug, log_error
from messaging.utils import send_sms
from system.models import Farmer, Collection
from payments.models import Transaction
from payments.utils import create_transaction
from conf.models import SMSTemplate, Product


@receiver(post_save, sender=Collection)
def create_collection_transaction(sender, instance, created, **kwargs):
    if created and instance.farmer:
        create_transaction(
            farmer=instance.farmer,
            amount=instance.total_price,
            tx_type='CREDIT',
            category=Transaction.CategoryOptions.COLLECTION
        )


@receiver(post_save, sender=Farmer)
def send_registration_sms(sender, instance, created, **kwargs):
    if created and instance.id:
        # Send SMS
        try:
            template = SMSTemplate.objects.get(code=SMSTemplate.TemplateCode.REGISTRATION)
            message = template.template.replace("<NAMES>", f"{instance.first_name} {instance.surname}")
            message = message.replace("<MEMBERID>", instance.member_id)
            send_sms(
                recipient=instance.phone_number,
                message=message,
            )
        except Exception as e:
            log_debug(f'Error Sending Registration SMS. {e}')
            log_error()


@receiver(post_save, sender=Collection)
def send_collection_sms(sender, instance, created, **kwargs):
    if created and instance.farmer:
        # Send SMS
        try:
            template = SMSTemplate.objects.get(code=SMSTemplate.TemplateCode.COLLECTION)
            message = template.template.replace("<NAMES>", f"{instance.farmer.first_name} {instance.farmer.surname}")
            message = message.replace("<PRODUCT>", instance.product.name)
            message = message.replace("<DETAILS>", f"Qty: {instance.quantity} Unit Price: {instance.unit_price} Total: {instance.total_price}")
            send_sms(
                recipient=instance.farmer.phone_number,
                message=message,
            )
        except Exception as e:
            log_debug(f'Error Sending Registration SMS. {e}')
            log_error()