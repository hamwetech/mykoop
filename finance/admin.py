from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.core.exceptions import ValidationError
from finance.models import (
    SharePurchase,
    SavingsTransaction,
    Loan,
    LoanRepayment,
    SocialFund,
    SocialFundContribution,
    Fine,
    CashBook,
    ShareOut
)

from finance.forms import LoanAdminForm


# -----------------------
# SHARE PURCHASE
# -----------------------
@admin.register(SharePurchase)
class SharePurchaseAdmin(admin.ModelAdmin):
    list_display = ("farmer", "date_purchased", "shares", "share_price", "amount", "total_cost", "shares_after", "created_at")
    search_fields = ("farmer__name",)
    list_filter = ("created_at",)


# -----------------------
# SAVINGS
# -----------------------
@admin.register(SavingsTransaction)
class SavingsTransactionAdmin(admin.ModelAdmin):
    list_display = ("farmer", "amount", "amount_after", "created_at")
    search_fields = ("farmer__name",)
    list_filter = ("created_at",)


# -----------------------
# LOANS
# -----------------------
class LoanRepaymentInline(admin.TabularInline):
    model = LoanRepayment
    extra = 0


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    form = LoanAdminForm
    list_display = (
        "farmer",
        "farmer_group",
        "amount",
        "interest_rate",
        "status",
        "issue_date",
        "due_date",
        "open_button"
    )
    list_filter = ("status", "farmer_group")
    search_fields = ("farmer__name", "purpose")
    inlines = [LoanRepaymentInline]

    def open_button(self, obj):
        url = reverse(
            "finance:loan-detail",
            args=[obj.id]
        )
        return format_html(
            '<a class="btn btn-success" style="background:#007bff;color:white;" href="{}">OPEN</a>',
            url
        )

    open_button.short_description = "Action"


# -----------------------
# LOAN REPAYMENT
# -----------------------
@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ("loan", "payment_date", "principal_paid", "interest_paid", "total_paid", "received_by")
    list_filter = ("payment_date",)


# -----------------------
# SOCIAL FUND
# -----------------------
@admin.register(SocialFund)
class SocialFundAdmin(admin.ModelAdmin):
    list_display = ("name", "farmer_group", "status", "target_amount", "start_date", "end_date", "open_button")
    list_filter = ("status", "farmer_group")
    search_fields = ("name",)

    def open_button(self, obj):
        url = reverse(
            "finance:loan-detail",
            args=[obj.id]
        )
        return format_html(
            '<a class="btn btn-success" style="background:#007bff;color:white;" href="{}">OPEN</a>',
            url
        )

    open_button.short_description = "Action"


@admin.register(SocialFundContribution)
class SocialFundContributionAdmin(admin.ModelAdmin):
    list_display = ("farmer", "social_fund", "amount", "created_at")
    list_filter = ("social_fund",)


# -----------------------
# FINES
# -----------------------
@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ("farmer", "social_fund", "reason", "amount", "paid", "created_at")
    list_filter = ("paid", "social_fund")
    search_fields = ("reason",)


# -----------------------
# CASHBOOK
# -----------------------
@admin.register(CashBook)
class CashBookAdmin(admin.ModelAdmin):
    list_display = ("transaction_date", "transaction_type", "description", "amount", "balance")
    list_filter = ("transaction_type", "transaction_date")
    search_fields = ("description",)


# -----------------------
# SHARE OUT
# -----------------------
@admin.register(ShareOut)
class ShareOutAdmin(admin.ModelAdmin):
    list_display = ("farmer", "total_shares", "total_savings", "interest_earned", "payout", "share_out_date")
    list_filter = ("share_out_date",)
    search_fields = ("farmer__name",)