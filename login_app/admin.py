from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'created_at', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('id', 'created_at', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(User, AccountAdmin)