from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):

    list_per_page = 25
    ordering = ("-id",)

    def get_list_display(self, request):
        fields = [field.name for field in self.model._meta.fields]

        if "id" not in fields:
            fields.insert(0, "id")

        return fields[:6]  # show first 6 fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # only when creating
            obj.created_by = request.user
        super().save_model(request, obj, form, change)