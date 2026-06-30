from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import User


class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'region'

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'district'

    def __str__(self):
        return self.name


class County(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'county'
        unique_together = ('district', 'name')

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sub_county'
        unique_together = ['county', 'name']

    def __str__(self):
        return self.name


class Parish(models.Model):
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parish'
        unique_together = ['sub_county', 'name']

    def __str__(self):
        return self.name


class Village(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'village'

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    method = models.CharField('Method', max_length=50)
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_method'

    def __str__(self):
        return self.method


class Crop(models.Model):
    name = models.CharField(max_length=25, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crop'

    def product_variation(self):
        return ProductVariation.objects.filter(product=self)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=25, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'

    def product_variation(self):
        return ProductVariation.objects.filter(product=self)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=25, unique=True)
    code = models.CharField(max_length=3, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'unit'
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        return self.name


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_variation'
        verbose_name = 'Product Variation'
        verbose_name_plural = 'Product Variation'
        unique_together = ['product', 'name']

    def __str__(self):
        return self.name


class ProductVariationPrice(models.Model):
    product = models.OneToOneField(ProductVariation, related_name='variation_price', on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_variation_price'
        verbose_name = 'Product Price'
        verbose_name_plural = 'Product Prices'
        unique_together = ['product', 'unit']

    def __str__(self):
        return "%s" % self.product


class ProductVariationPriceLog(models.Model):
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_variation_price_log'
        verbose_name = 'Product Price Log'
        verbose_name_plural = 'Product Price Logs'

    def __unicode__(self):
        return "%s" % self.product


class Profession(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=120)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profession'
        verbose_name = 'Profession'
        verbose_name_plural = 'Professions'


@receiver(post_save, sender=ProductVariationPrice)
def save_price_log(sender, instance, **kwargs):
    ProductVariationPriceLog.objects.create(product=instance.product,
                                                price=instance.price,
                                            unit=instance.unit,
                                            created_by=instance.created_by)


class MessageTemplates(models.Model):
    collection = models.TextField(null=True, blank=True)
    coop_share_purchase = models.TextField(null=True, blank=True)
    member_share_purchase = models.TextField(null=True, blank=True)
    member_registration = models.TextField(null=True, blank=True)
    purchase_confirmation = models.TextField(null=True, blank=True)
    payment_confirmation = models.TextField(null=True, blank=True)
    supply_request = models.TextField(null=True, blank=True)
    supply_confirmation = models.TextField(null=True, blank=True)
    supply_cancelled = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'message_template'

    def __str__(self):
        return u'Messages Template'


class SMSTemplate(models.Model):
    class TemplateCode(models.TextChoices):
        REGISTRATION = 'REGISTRATION' 'REGISTRATION'
        COLLECTION = 'COLLECTION' 'COLLECTION'
        ORDER = 'ORDER' 'ORDER'
        ORDER_CONFIRMATION = 'ORDER_CONFIRMATION' 'ORDER_CONFIRMATION'
        ORDER_SHIPPING = 'ORDER_SHIPPING' 'ORDER_SHIPPING'
        ORDER_PICKING_READY = 'ORDER_PICKING_READY' 'ORDER_PICKING_READY'


    code = models.CharField(max_length=120, unique=True, choices=TemplateCode.choices, null=True)
    template = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   null = True,
                                   blank = True,
                                   editable = False
                                   )

    class Meta:
        db_table = 'sms_template'


class SystemConfiguration(models.Model):
    send_sms = models.BooleanField(default=0)
    send_email = models.BooleanField(default=0)
    report_recipient_email = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'system_configuration'



class EmailConfiguration(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
