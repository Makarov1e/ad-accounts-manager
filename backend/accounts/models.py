"""Domain model for advertising accounts (рекламные кабинеты)."""

from django.db import models


class AccountType(models.TextChoices):
    AGENCY = "agency", "Agency"
    BM = "bm", "BM"
    PERSONAL = "personal", "Personal"


class Department(models.TextChoices):
    DEPARTMENT_1 = "dep_1", "Отдел 1"
    DEPARTMENT_2 = "dep_2", "Отдел 2"


class AccountStatus(models.TextChoices):
    ISSUED = "issued", "Выдан"
    IN_WORK = "in_work", "В работе"
    BAN = "ban", "Бан"
    RETURN = "return", "Возврат"


#: Ordered lifecycle used by the "advance status" action: Выдан → В работе → Бан → Возврат.
STATUS_FLOW = [
    AccountStatus.ISSUED,
    AccountStatus.IN_WORK,
    AccountStatus.BAN,
    AccountStatus.RETURN,
]

#: Statuses considered "dead" for dashboard/returns purposes.
INACTIVE_STATUSES = {AccountStatus.BAN, AccountStatus.RETURN}


class Account(models.Model):
    """A single advertising account being tracked.

    ``account_id`` is the human-facing identifier (e.g. ``act_123456``); it is
    free-form on purpose per the spec and is not used as the primary key.
    """

    account_id = models.CharField("ID кабинета", max_length=120, db_index=True)
    type = models.CharField(
        "Тип", max_length=20, choices=AccountType.choices, default=AccountType.PERSONAL
    )
    seller = models.CharField("Селлер", max_length=120)
    department = models.CharField(
        "Отдел", max_length=20, choices=Department.choices, default=Department.DEPARTMENT_1
    )
    status = models.CharField(
        "Статус", max_length=20, choices=AccountStatus.choices, default=AccountStatus.ISSUED
    )
    created_at = models.DateTimeField("Дата", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Рекламный кабинет"
        verbose_name_plural = "Рекламные кабинеты"

    def __str__(self) -> str:
        return f"{self.account_id} ({self.get_status_display()})"

    def advance_status(self) -> str:
        """Move one step forward along :data:`STATUS_FLOW`, wrapping at the end.

        Returns the new status value. Purely manual — only ever called from an
        explicit user action, never automatically.
        """
        current = AccountStatus(self.status)
        index = STATUS_FLOW.index(current)
        self.status = STATUS_FLOW[(index + 1) % len(STATUS_FLOW)].value
        return self.status
