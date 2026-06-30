from django.db import models, transaction
from django.contrib.auth.models import User
from system.models.farmer import Farmer, FarmerGroup
from system.models.modelmixin import TimeStampMixin


class SharePurchase(TimeStampMixin):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE
    )
    date_purchased = models.DateField(null=True)
    shares = models.PositiveIntegerField()
    share_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shares_after = models.PositiveIntegerField(editable=False)

    class Meta:
        db_table = 'share_purchase'
        verbose_name = 'Share Purchase'
        verbose_name_plural = 'Share Purchase'

    @property
    def amount(self):
        return self.shares * self.share_price
    
    def save(self, *args, **kwargs):
        account, created = Farmer.objects.get_or_create(
            pk=self.farmer.pk
        )
        account.shares_balance += self.shares
        account.save()

        self.shares_after = account.shares_balance

        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.farmer)


class SavingsTransaction(TimeStampMixin):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField(blank=True)
    amount_after = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)

    class Meta:
        db_table = 'savings_transaction'
        verbose_name = 'Savings Transaction'
        verbose_name_plural = 'Savings Transactions'


    def save(self, *args, **kwargs):
        account, created = Farmer.objects.get_or_create(
            pk=self.farmer.pk
        )
        account.savings_balance += self.amount
        account.save()

        self.amount_after = account.savings_balance

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.farmer} - {self.amount}"


class LoanManager(models.Manager):

    def create_loan(self, farmer, **kwargs):

        active = self.filter(
            farmer=farmer
        ).exclude(
            status__in=["Completed", "Rejected"]
        )

        if active.exists():
            raise ValueError("Active loan already exists")

        return self.create(farmer=farmer, **kwargs)  


class Loan(TimeStampMixin):
    STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
        ("Defaulted", "Defaulted"),
    )

    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE
    )
    farmer_group = models.ForeignKey(FarmerGroup, verbose_name="VSLA", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10
    )
    total_repaid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    purpose = models.CharField(max_length=255)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="loan_approver"
    )

    objects = LoanManager()

    class Meta:
        db_table = 'loan'
        verbose_name = 'Loan'
        verbose_name_plural = 'Loan'

    def __str__(self):
        return f"{self.farmer} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            interest = (self.amount * self.interest_rate) / 100
            self.balance = self.amount + interest
        super().save(*args, **kwargs)


class LoanRepayment(TimeStampMixin):
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="repayments"
    )
    payment_date = models.DateField()
    principal_paid = models.DecimalField(max_digits=12, decimal_places=2)
    interest_paid = models.DecimalField(max_digits=12, decimal_places=2)
    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="repayment_receiver"
    )

    class Meta:
        db_table = 'loan_repayment'
        verbose_name = 'Loan Repayment'
        verbose_name_plural = 'Loan Repayments'

    @property
    def total_paid(self):
        return self.principal_paid + self.interest_paid
    

    def save(self, *args, **kwargs):
        with transaction.atomic():

            # 1. Save repayment first
            super().save(*args, **kwargs)

            loan = self.loan

            # 2. Calculate totals
            totals = loan.repayments.aggregate(
                principal=models.Sum("principal_paid"),
                interest=models.Sum("interest_paid")
            )

            total_principal = totals["principal"] or 0
            total_interest = totals["interest"] or 0

            total_repaid = total_principal + total_interest

            # 3. Update loan
            loan.total_repaid = total_repaid
            loan.balance = (loan.amount + (loan.amount * loan.interest_rate / 100)) - total_repaid

            # 4. Mark completed if fully paid
            if loan.balance <= 0:
                loan.status = "Completed"
                loan.balance = 0

            loan.save()


class SocialFund(TimeStampMixin):
    STATUS = (
        ("Active", "Active"),
        ("Disabled", "Disabled"),
        ("Suspended", "Suspended")
    )
    farmer_group = models.ForeignKey(FarmerGroup, verbose_name="VSLA", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=120, choices=STATUS, default='Active')
    target_amount = models.DecimalField(decimal_places=2, max_digits=32)

    class Meta:
        db_table = 'social_fund'
        verbose_name = 'Social Fund'
        verbose_name_plural = 'Social Funds'


class SocialFundContribution(TimeStampMixin):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE
    )
    social_fund = models.ForeignKey(
        SocialFund,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'social_fund_contribution'
        verbose_name = 'Social Fund Contribution'
        verbose_name_plural = 'Social Fund Contributions'

    def __str__(self):
        return f"{self.farmer}"


class Fine(TimeStampMixin):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE
    )
    social_fund = models.ForeignKey(
        SocialFund,
        on_delete=models.CASCADE
    )
    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member}"


class CashBook(TimeStampMixin):
    TRANSACTION_TYPES = (
        ("Income", "Income"),
        ("Expense", "Expense"),
    )

    transaction_date = models.DateField()
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.transaction_date} - {self.transaction_type}"


class ShareOut(TimeStampMixin):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE
    )
    total_shares = models.PositiveIntegerField()
    total_savings = models.DecimalField(max_digits=12, decimal_places=2)
    interest_earned = models.DecimalField(max_digits=12, decimal_places=2)
    payout = models.DecimalField(max_digits=12, decimal_places=2)
    share_out_date = models.DateField()

    def __str__(self):
        return str(self.member)
