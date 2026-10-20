from datetime import date
from django.db.models import Sum

from .models import (
    Loan,
    SharePurchase,
    SavingsTransaction,
    Fine,
    SocialFundContribution,
    Attendance,
)


class CreditScoreService:

    def __init__(self, farmer):
        self.farmer = farmer

    def calculate(self):
        score = 0

        score += self.savings_score()
        score += self.share_score()
        score += self.repayment_score()
        score += self.attendance_score()
        score += self.social_fund_score()
        score += self.membership_score()

        score -= self.fine_penalty()

        return max(0, min(score, 100))

    def savings_score(self):
        savings = SavingsTransaction.objects.filter(
            farmer=self.farmer
        ).aggregate(total=Sum("amount"))["total"] or 0

        if savings >= 1_000_000:
            return 30
        elif savings >= 500_000:
            return 20
        elif savings >= 100_000:
            return 10

        return 0

    def share_score(self):
        shares = SharePurchase.objects.filter(
            farmer=self.farmer
        ).aggregate(total=Sum("shares"))["total"] or 0

        if shares >= 100:
            return 15
        elif shares >= 50:
            return 10

        return 5 if shares else 0

    def repayment_score(self):
        defaults = Loan.objects.filter(
            farmer=self.farmer,
            status="Defaulted"
        ).count()

        return 25 if defaults == 0 else 0

    def attendance_score(self):
        total = Attendance.objects.filter(
            farmer=self.farmer
        ).count()

        if total == 0:
            return 0

        attended = Attendance.objects.filter(
            farmer=self.farmer,
            present=True
        ).count()

        percentage = attended / total

        if percentage >= 0.90:
            return 10
        elif percentage >= 0.75:
            return 7

        return 4

    def social_fund_score(self):
        total = SocialFundContribution.objects.filter(
            farmer=self.farmer
        ).aggregate(total=Sum("amount"))["total"] or 0

        return 10 if total > 0 else 0

    def membership_score(self):
        years = (date.today() - self.farmer.date_joined).days / 365

        if years >= 2:
            return 10
        elif years >= 1:
            return 5

        return 0

    def fine_penalty(self):
        fines = Fine.objects.filter(
            farmer=self.farmer,
            paid=False
        ).count()

        return min(fines * 2, 10)