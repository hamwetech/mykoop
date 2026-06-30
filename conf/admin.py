from django.contrib import admin
from django.apps import apps
from django.shortcuts import redirect
from conf.base_admin import BaseAdmin
from conf.models import SystemConfiguration


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        # Allow add only if no record exists
        return not SystemConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SystemConfiguration.objects.first()

        if obj:
            return redirect(f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/{obj.id}/change/')
        else:
            return redirect(f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/add/')


app_models = apps.get_app_config("conf").get_models()

for model in app_models:
    try:
        admin.site.register(model, BaseAdmin)
    except admin.sites.AlreadyRegistered:
        pass
