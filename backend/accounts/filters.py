"""Filtering for the accounts list endpoint."""

from django_filters import rest_framework as filters

from .models import Account, AccountStatus


class AccountFilter(filters.FilterSet):
    """Filter accounts by department, type and status.

    ``status`` accepts multiple values (``?status=ban&status=return``) so the
    Returns page can request banned + returned accounts in one call, while the
    table still works with a single selected status.
    """

    status = filters.MultipleChoiceFilter(choices=AccountStatus.choices)

    class Meta:
        model = Account
        fields = ["department", "type", "status"]
