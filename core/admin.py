from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NGO, Project, Workforce, Permit

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("role",)}),)

admin.site.register(User, CustomUserAdmin)
admin.site.register(NGO)
admin.site.register(Project)
admin.site.register(Workforce)
admin.site.register(Permit)
