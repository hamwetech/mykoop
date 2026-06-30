import openpyxl
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ExcelUploadForm
from .models import District, County, SubCounty, Parish, Village, ProductVariation, ProductVariationPrice


def upload_locations(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["file"]
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            # Assuming first row has headers
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                district_name, county_name, subcounty_name, parish_name, village_name = row

                if not district_name:
                    messages.warning(request, f"Row {i}: Missing district, skipping.")
                    continue

                # Create hierarchy
                district, _ = District.objects.get_or_create(name=district_name)
                county, _ = County.objects.get_or_create(name=county_name, district=district)
                subcounty, _ = SubCounty.objects.get_or_create(name=subcounty_name, county=county)
                parish, _ = Parish.objects.get_or_create(name=parish_name, sub_county=subcounty)
                Village.objects.get_or_create(name=village_name, parish=parish)

            messages.success(request, "Excel file uploaded successfully!")
            return redirect("/admin")
    else:
        form = ExcelUploadForm()

    return render(request, "admin/upload_locations.html", {"form": form, "subtitle": "Location", "title": "Location"})


def get_product_price(request, pk):
    product = ProductVariationPrice.objects.get(product__id=pk)
    return JsonResponse({'price': str(product.price)})