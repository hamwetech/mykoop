from django.shortcuts import render
from datetime import date
from django.http import JsonResponse
from django.db.models import Sum
from django.views.generic import View, DetailView
from django.db.models import Count, Q, Case, When, IntegerField
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncWeek
from django.shortcuts import get_object_or_404

from sales.models import Order
from messaging.models import SmsLog
from system.models import Farmer, Clan, Collection, AppVersion, FarmerGroup
from finance.models import Loan, LoanRepayment


def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # total_farmers = Farmer.objects.count()
        #
        # total_male = Farmer.objects.filter(gender='Male').count()
        # total_female = Farmer.objects.filter(gender='Female').count()
        # total_clans_with_farmers = Clan.objects.annotate(
        #     farmer_count=Count('farmer')
        # ).filter(farmer_count__gt=0).count()
        #
        # today = date.today()
        #
        # farmers = Farmer.objects.exclude(date_of_birth__isnull=True)
        #
        # youths = farmers.filter(
        #     date_of_birth__gt=date(today.year - 35, today.month, today.day)
        # ).count()
        #
        # adults = farmers.filter(
        #     date_of_birth__lte=date(today.year - 35, today.month, today.day)
        # ).count()
        #
        # youth_male = farmers.filter(
        #     gender='Male',
        #     date_of_birth__gt=date(today.year - 35, today.month, today.day)
        # ).count()
        #
        # youth_female = farmers.filter(
        #     gender='Female',
        #     date_of_birth__gt=date(today.year - 35, today.month, today.day)
        # ).count()
        #
        # adult_male = farmers.filter(
        #     gender='Male',
        #     date_of_birth__lte=date(today.year - 35, today.month, today.day)
        # ).count()
        #
        # adult_female = farmers.filter(
        #     gender='Female',
        #     date_of_birth__lte=date(today.year - 35, today.month, today.day)
        # ).count()
        #
        # farmers_per_clan = Farmer.objects.values('clan__name').annotate(
        #     total=Count('id')
        # ).order_by('-total')
        #
        # farmers_per_district = Farmer.objects.values('district__name').annotate(
        #     total=Count('id')
        # ).order_by('-total')
        #
        # farmers_per_clan_district = Farmer.objects.values(
        #     'district__name', 'clan__name'
        # ).annotate(
        #     total=Count('id')
        # ).order_by('district__name', '-total')

        today = date.today()
        farmers = Farmer.objects.all()
        orders = Order.objects.all()
        collections = Collection.objects.all()
        total_vsla = FarmerGroup.objects.all()
        
        total_shares = farmers.aggregate(
            total=Sum('shares_balance')
        )

        total_savings = farmers.aggregate(
            total=Sum('savings_balance')
        )

        pending_summary = Loan.objects.filter(
            status="Pending"
        ).aggregate(
            total_amount=Sum("amount"),
            total_count=Count("id")
        )

        loan_requests = Loan.objects.filter(
            status="Approved"
        ).aggregate(
            total_amount=Sum("amount"),
            total_count=Count("id")
        )

        # if self.request.user.userprofile.clan:
        #     clan = self.request.user.userprofile.clan
        #     farmers = farmers.filter(clan=clan)
        #     collections = collections.filter(farmer__clan=clan)
        #     orders = orders.filter(farmer__clan=clan)

        youth_male = farmers.filter(
            gender='Male',
            date_of_birth__gt=date(today.year - 35, today.month, today.day)
        ).count()

        youth_female = farmers.filter(
            gender='Female',
            date_of_birth__gt=date(today.year - 35, today.month, today.day)
        ).count()

        adult_male = farmers.filter(
            gender='Male',
            date_of_birth__lte=date(today.year - 35, today.month, today.day)
        ).count()

        adult_female = farmers.filter(
            gender='Female',
            date_of_birth__lte=date(today.year - 35, today.month, today.day)
        ).count()

        orders = orders.count()
        collections = collections.count()
        sms_count = SmsLog.objects.filter(status='SENT').count()

        data = {
            "total_farmers": farmers.count(),
            "total_male": farmers.filter(gender='Male').count(),
            "total_female": farmers.filter(gender='Female').count(),
            "orders": orders,
            "collections": collections,
            "total_vsla": total_vsla.count(),
            "sms_count": sms_count,
            "total_shares": total_shares.get('total'),
            "total_savings": total_savings.get('total'),
            "pending_summary": pending_summary,
            "loan_requests": loan_requests,
            "total_clans_with_farmers": Clan.objects.annotate(
                farmer_count=Count('farmer')
            ).filter(farmer_count__gt=0).count(),

            "youths": farmers.filter(
                date_of_birth__gt=date(today.year - 35, today.month, today.day)
            ).count(),

            "adults": farmers.filter(
                date_of_birth__lte=date(today.year - 35, today.month, today.day)
            ).count(),

            "youth_male": youth_male,
            "youth_female": youth_female,
            "adult_male": adult_male,
            "adult_female": adult_female,

            "per_clan": list(
                farmers.values('clan__name').annotate(total=Count('id'))
            ),

            "per_district": list(
                farmers.values('district__name').annotate(total=Count('id'))
            ),

            "per_clan_district": list(
                farmers.values('district__name', 'clan__name')
                .annotate(total=Count('id'))
            )
        }
        context.update(data)

        return context


def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

class GenderStatsView(View):
    def get(self, request, *args, **kwargs):
        base = {'Male': 0, 'Female': 0}

        data = Farmer.objects.values('gender').annotate(total=Count('id'))

        for item in data:
            gender = item['gender']
            if gender in base:
                base[gender] = item['total']

        return JsonResponse({
            "labels": list(base.keys()),
            "data": list(base.values())
        })


class DemographicStatsView(View):
    def get(self, request, *args, **kwargs):
        base = {'Male': 0, 'Female': 0}

        data = Farmer.objects.values('gender').annotate(total=Count('id'))

        for item in data:
            gender = item['gender']
            if gender in base:
                base[gender] = item['total']

        return JsonResponse({
            "labels": list(base.keys()),
            "data": list(base.values())
        })


class FarmerMonthlyStatsView(View):
    def get(self, request, *args, **kwargs):
        data = (
            Farmer.objects
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )

        labels = []
        values = []

        for item in data:
            labels.append(item['month'].strftime('%b %Y'))  # Jan 2026
            values.append(item['total'])

        return JsonResponse({
            "labels": labels,
            "datasets": [{
                "label": "Farmers per Month",
                "data": values,
                "backgroundColor": "#28a745"
            }]
        })


class FarmerWeeklyStatsView(View):
    def get(self, request, *args, **kwargs):
        data = (
            Farmer.objects
            .annotate(week=TruncWeek('created_at'))
            .values('week')
            .annotate(total=Count('id'))
            .order_by('week')
        )

        labels = []
        values = []

        for item in data:
            labels.append(item['week'].strftime('Week %W (%b %d)'))
            values.append(item['total'])

        return JsonResponse({
            "labels": labels,
            "datasets": [{
                "label": "Farmers per Week",
                "data": values,
                "backgroundColor": "#007bff"
            }]
        })


import openpyxl
from django.http import HttpResponse
from system.models import Farmer

def export_farmers_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Farmers"

    # 🔹 Header
    headers = [
        "Member ID", "Name", "Gender", "Phone",
        "District", "County", "SubCounty", "Parish",
        "Village", "Account Balance", "Savings",
        "DOB", "Created At"
    ]

    ws.append(headers)

    # 🔹 Data
    farmers = Farmer.objects.select_related(
        'district', 'county', 'sub_county', 'parish'
    ).all()

    for f in farmers:
        name = f"{f.title or ''} {f.first_name or ''} {f.surname or ''}".strip()

        ws.append([
            f.member_id,
            name,
            f.gender,
            f.phone_number,
            f.district.name if f.district else "",
            f.county.name if f.county else "",
            f.sub_county.name if f.sub_county else "",
            f.parish.name if f.parish else "",
            f.village,
            float(f.account_balance or 0),
            float(f.savings_balance or 0),
            f.date_of_birth.strftime('%Y-%m-%d') if f.date_of_birth else "",
            f.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    # 🔹 Auto column width
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2

    # 🔹 Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=farmers.xlsx'

    wb.save(response)
    return response

class AppDownloadView(DetailView):
    model = AppVersion
    template_name = "app/download.html"
    context_object_name = "app"

    def get_object(self):
        return AppVersion.objects.filter(is_active=True).order_by("-version_code").first()