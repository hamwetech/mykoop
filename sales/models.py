import uuid
from django.db import models

from conf.models import Unit
from system.models import TimeStampMixin, Farmer, Cooperative


class Supplier(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'supplier'

    def __str__(self):
        return self.name


class Category(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Item(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='items')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'item'

    def __str__(self):
        return self.name


class Order(TimeStampMixin):
    cooperative = models.ForeignKey(Cooperative, null=True, blank=True, on_delete=models.SET_NULL)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    order_reference = models.CharField(max_length=255, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=255, default='PENDING')
    order_date = models.DateTimeField()
    accept_date = models.DateTimeField(null=True, blank=True)
    reject_date = models.DateTimeField(null=True, blank=True)
    reject_reason = models.CharField(max_length=120, null=True, blank=True)
    ship_date = models.DateTimeField(null=True, blank=True)
    delivery_accept_date = models.DateTimeField(null=True, blank=True)
    delivery_reject_date = models.DateTimeField(null=True, blank=True)
    delivery_reject_reason = models.CharField(max_length=120, null=True, blank=True)
    collect_date = models.DateTimeField(null=True, blank=True)
    gps_coordinates = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'member_order'

    def save(self, *args, **kwargs):
        if not self.order_reference:
            self.order_reference = f"COL-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % self.order_reference or u''

    def get_orders(self):
        return OrderItem.objects.filter(order=self)


class OrderItem(TimeStampMixin):
    order = models.ForeignKey(Order, blank=True, on_delete=models.CASCADE, related_name='items',)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    order_reference = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'order_item'

    def __str__(self):
        return "%s" % self.item or u''