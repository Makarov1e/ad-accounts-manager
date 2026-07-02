"""DRF serializers for the accounts API."""

from rest_framework import serializers

from .models import Account, AccountType, Department


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


class AccountBulkCreateSerializer(serializers.Serializer):
    """Create several accounts at once from a list of ids sharing the same
    type / seller / department."""

    account_ids = serializers.ListField(
        child=serializers.CharField(max_length=120), allow_empty=False
    )
    type = serializers.ChoiceField(choices=AccountType.choices)
    seller = serializers.CharField(max_length=120)
    department = serializers.ChoiceField(choices=Department.choices)

    def validate_account_ids(self, value: list[str]) -> list[str]:
        cleaned, seen = [], set()
        for raw in value:
            item = raw.strip()
            if item and item not in seen:
                seen.add(item)
                cleaned.append(item)
        if not cleaned:
            raise serializers.ValidationError("Укажите хотя бы один ID кабинета.")
        return cleaned

    def validate_seller(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Укажите селлера.")
        return value

    def create(self, validated_data: dict) -> list[Account]:
        accounts = [
            Account(
                account_id=account_id,
                type=validated_data["type"],
                seller=validated_data["seller"],
                department=validated_data["department"],
            )
            for account_id in validated_data["account_ids"]
        ]
        return Account.objects.bulk_create(accounts)
