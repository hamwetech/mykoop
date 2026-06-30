from django import forms
from os.path import splitext
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from ..models import Farmer


class FarmerAdminForm(forms.ModelForm):

    class Meta:
        model = Farmer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(FarmerAdminForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column("name", css_class="col-md-6"),
                Column("gender", css_class="col-md-6"),
            ),
            Row(
                Column("phone_number", css_class="col-md-6"),
                Column("village", css_class="col-md-6"),
            ),
        )


class ClanUploadForm(forms.Form):
    sheetChoice = (
        ('1', 'sheet1'),
        ('2', 'sheet2'),
        ('3', 'sheet3'),
        ('4', 'sheet4'),
        ('5', 'sheet5'),
    )

    rowchoices = (
        ('1', 'Row 1'),
        ('2', 'Row 2'),
        ('3', 'Row 3'),
        ('4', 'Row 4'),
        ('5', 'Row 5')
    )

    choices = list()
    for i in range(65, 91):
        choices.append([i - 65, chr(i)])

    excel_file = forms.FileField()
    sheet = forms.ChoiceField(label="Sheet", choices=sheetChoice, widget=forms.Select(attrs={'class': 'form-control'}))
    row = forms.ChoiceField(label="Row", choices=rowchoices, widget=forms.Select(attrs={'class': 'form-control'}))
    name_col = forms.ChoiceField(label='Name Column', initial=0, choices=choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text='The column containing the Clan Names')
    totem_col = forms.ChoiceField(label='Totem Column', initial=1, choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                     help_text='The column containing the Totem')

    def clean(self):
        data = self.cleaned_data
        f = data.get('excel_file', None)
        ext = splitext(f.name)[1][1:].lower()
        if not ext in ["xlsx", "xls"]:
            raise forms.ValidationError(("the File type is not accepted"))
        return data