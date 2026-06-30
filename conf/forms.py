from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        label="Select Excel file",
        help_text="Upload .xlsx file with headers: district, county, subcounty, parish, village"
    )