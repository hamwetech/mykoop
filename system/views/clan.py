import re
import json
import xlrd
import datetime
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Count, Q, Case, When, IntegerField
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from conf.utils import log_error
from system.forms import ClanUploadForm
from system.models import Farmer, Clan


class ClanUploadView(View):
    template_name = 'admin/system/collection_upload.html'

    def get(self, request, *arg, **kwargs):
        data = dict()
        data['form'] = ClanUploadForm
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = dict()
        form = ClanUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['excel_file']

            # path = f.temporary_file_path()
            index = int(form.cleaned_data['sheet']) - 1
            startrow = int(form.cleaned_data['row']) - 1
            name_col = int(form.cleaned_data['name_col'])
            totem_col = int(form.cleaned_data['totem_col'])

            book = xlrd.open_workbook(file_contents=f.read())
            # book = xlrd.open_workbook(filename=path, logfile='/tmp/xls.log')
            sheet = book.sheet_by_index(index)
            rownum = 0
            data = dict()
            clan_list = []
            for i in range(startrow, sheet.nrows):
                try:
                    row = sheet.row(i)
                    rownum = i + 1
                    name = smart_str(row[name_col].value).strip()

                    if not re.search('^[A-Z\s\(\)\-\.]+$', name, re.IGNORECASE):
                        data['errors'] = '"%s" is not a valid Name (row %d)' % \
                                         (name, i + 1)
                        return render(request, self.template_name, {'active': 'system', 'form': form, 'error': data})


                    totem = smart_str(row[totem_col].value).strip()
                    if isinstance(totem, str):
                        # totem = totem.decode('utf-8', 'ignore')
                        totem = totem.encode("utf-8", "ignore").decode("utf-8")

                    # totem = totem.encode('ascii', 'ignore')
                    if totem:
                        totem = re.sub(r"[^\w\s\(\)\-\.,\/']", "", totem)
                        # print(totem)
                        # if not re.search('^[A-Z\s\(\)\-\.\,\/\']+$', totem, re.IGNORECASE):
                        #     data['errors'] = '"%s" is not a valid Totem (row %d)' % \
                        #                      (totem, i + 1)
                        #     return render(request, self.template_name,
                        #                   {'active': 'system', 'form': form, 'error': data})

                    q = {'name': name, 'totem': totem}
                    clan_list.append(q)

                except Exception as err:
                    log_error()
                    print(f"ERROR PROCESSING {err}")
                    return render(request, self.template_name, {'active': 'setting', 'form': form, 'error': err})
            if clan_list:
                with transaction.atomic():
                    try:
                        do = None
                        sco = None
                        for c in clan_list:
                            name = c.get('name')
                            totem = c.get('totem')

                            if not Clan.objects.filter(name=name).exists():

                                Clan(
                                    name=name,
                                    totem=totem,
                                    created_by=self.request.user
                                ).save()

                        return redirect('admin:system_clan_changelist')
                    except Exception as err:
                        log_error()
                        print(err)
                        data['error'] = err

        data['form'] = form
        return render(request, self.template_name, data)