"""Django admin registration for accounts."""

from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_id", "type", "seller", "department", "status", "created_at")
    list_filter = ("type", "department", "status")
    search_fields = ("account_id", "seller")
    ordering = ("-created_at",)
