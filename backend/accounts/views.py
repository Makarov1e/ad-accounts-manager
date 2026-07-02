"""API views for advertising accounts."""

import csv

from django.db.models import Count
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .constants import SELLERS
from .filters import AccountFilter
from .models import (
    Account,
    AccountStatus,
    AccountType,
    Department,
    INACTIVE_STATUSES,
)
from .serializers import AccountBulkCreateSerializer, AccountSerializer


def _choices_payload(choices) -> list[dict[str, str]]:
    """Serialise a ``TextChoices`` enum as ``[{value, label}, ...]``."""
    return [{"value": value, "label": label} for value, label in choices]


class AccountViewSet(viewsets.ModelViewSet):
    """CRUD for accounts plus dashboard, status and export helpers.

    Query params on ``list``/``export``:
      * ``department``, ``type``, ``status`` (repeatable) — exact filters
      * ``search`` — matches ``account_id``
      * ``ordering`` — e.g. ``-created_at``, ``account_id``
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filterset_class = AccountFilter
    search_fields = ["account_id"]
    ordering_fields = ["created_at", "account_id", "status", "seller"]
    ordering = ["-created_at"]

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        """Create several accounts in one request (shared type/seller/department)."""
        serializer = AccountBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = serializer.save()
        data = AccountSerializer(created, many=True).data
        return Response(
            {"created": len(data), "accounts": data}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def advance(self, request, pk=None):
        """Advance the account one step along the status lifecycle."""
        account = self.get_object()
        account.advance_status()
        account.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(account).data)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """Dashboard summary: totals, alive/banned, and a per-department breakdown."""
        queryset = Account.objects.all()
        by_status = {
            row["status"]: row["count"]
            for row in queryset.values("status").annotate(count=Count("id"))
        }
        total = sum(by_status.values())
        banned = by_status.get(AccountStatus.BAN, 0)
        returned = by_status.get(AccountStatus.RETURN, 0)

        departments = []
        for value, label in Department.choices:
            dept_qs = queryset.filter(department=value)
            dept_total = dept_qs.count()
            dept_inactive = dept_qs.filter(status__in=INACTIVE_STATUSES).count()
            departments.append(
                {
                    "value": value,
                    "label": label,
                    "total": dept_total,
                    "alive": dept_total - dept_inactive,
                    "inactive": dept_inactive,
                }
            )

        return Response(
            {
                "total": total,
                "alive": total - banned - returned,
                "banned": banned,
                "returned": returned,
                "by_status": [
                    {"value": value, "label": label, "count": by_status.get(value, 0)}
                    for value, label in AccountStatus.choices
                ],
                "by_department": departments,
            }
        )

    @action(detail=False, methods=["get"])
    def export(self, request):
        """Stream the currently filtered accounts as a CSV download."""
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="accounts.csv"'
        response.write("﻿")  # BOM so Excel opens UTF-8 correctly

        writer = csv.writer(response)
        writer.writerow(["ID", "Тип", "Селлер", "Отдел", "Статус", "Дата"])
        for account in queryset:
            writer.writerow(
                [
                    account.account_id,
                    account.get_type_display(),
                    account.seller,
                    account.get_department_display(),
                    account.get_status_display(),
                    account.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )
        return response

    @action(detail=False, methods=["get"])
    def meta(self, request):
        """Choices and seller suggestions used to build the add form."""
        return Response(
            {
                "types": _choices_payload(AccountType.choices),
                "departments": _choices_payload(Department.choices),
                "statuses": _choices_payload(AccountStatus.choices),
                "sellers": SELLERS,
            }
        )
