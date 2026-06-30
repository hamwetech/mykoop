from django.contrib import admin

from payments.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'farmer',
        'category',
        'amount',
        'balance',
        'transaction_date',
    )

    list_filter = (
        'category',
        'transaction_date',
    )

    search_fields = (
        'farmer__name',
        'transaction_reference',
    )

    ordering = ('-transaction_date',)

    readonly_fields = (
        'balance',
        'transaction_date',
    )

    list_per_page = 20


