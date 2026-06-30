from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

# -------------------------
# Inline for UserProfile
# -------------------------
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    extra = 1
    exclude = ('create_date',)


# -------------------------
# Extend default UserAdmin
# -------------------------
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')
    list_select_related = ('userprofile',)

    # Display fields from UserProfile
    def get_phone(self, instance):
        return instance.userprofile.phone_number if hasattr(instance, 'userprofile') else '-'
    get_phone.short_description = 'Phone'


# -------------------------
# Unregister default User and register custom
# -------------------------
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
