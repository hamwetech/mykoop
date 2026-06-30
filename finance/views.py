from django.shortcuts import render

from django.shortcuts import get_object_or_404, render
from django.db.models import Sum, F
from finance.models import Loan

def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk)

    repayments = loan.repayments.all()

    totals = repayments.aggregate(
        principal=Sum("principal_paid"),
        interest=Sum("interest_paid")
    )

    total_principal = totals["principal"] or 0
    total_interest = totals["interest"] or 0

    total_repaid = total_principal + total_interest

    loan_amount_with_interest = loan.amount + (loan.amount * loan.interest_rate / 100)

    balance = loan_amount_with_interest - total_repaid

    context = {
        "loan": loan,
        "repayments": repayments,
        "total_principal": total_principal,
        "total_interest": total_interest,
        "total_repaid": total_repaid,
        "balance": balance,
        "loan_total": loan_amount_with_interest,
    }

    return render(request, "finance/loan_detail.html", context)
