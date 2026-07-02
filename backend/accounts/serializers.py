"""DRF serializers for the accounts API."""

from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Read/write representation of an account.

    Alongside the raw enum values the payload carries ``*_display`` labels so
    the frontend can render the Russian captions without duplicating the
    choice map.
    """

    type_display = serializers.CharField(source="get_type_display", read_only=True)
    department_display = serializers.CharField(source="get_department_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "account_id",
            "type",
            "type_display",
            "seller",
            "department",
            "department_display",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_account_id(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("ID кабинета не может быть пустым.")
        return value

    def validate_seller(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Укажите селлера.")
        return value
