"""Populate the database with fictional demo accounts.

Usage::

    python manage.py seed            # add 16 random accounts
    python manage.py seed --count 20 # add a specific number
    python manage.py seed --fresh    # wipe existing accounts first
"""

import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.constants import SELLERS
from accounts.models import Account, AccountStatus, AccountType, Department


class Command(BaseCommand):
    help = "Seed the database with random demo advertising accounts."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=16, help="How many accounts to create.")
        parser.add_argument(
            "--fresh", action="store_true", help="Delete existing accounts before seeding."
        )

    def handle(self, *args, **options):
        count = options["count"]
        if options["fresh"]:
            deleted, _ = Account.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Removed {deleted} existing rows."))

        types = [choice.value for choice in AccountType]
        departments = [choice.value for choice in Department]
        statuses = [choice.value for choice in AccountStatus]
        now = timezone.now()

        # Guarantee at least two accounts per status so every state is visible
        # on first open, then fill the remainder with a weighted random spread.
        planned_statuses = [status for status in statuses for _ in range(2)]
        while len(planned_statuses) < count:
            planned_statuses.append(random.choices(statuses, weights=[4, 5, 2, 2])[0])
        random.shuffle(planned_statuses)

        accounts = []
        for status in planned_statuses[:count]:
            created = now - timezone.timedelta(
                days=random.randint(0, 45), minutes=random.randint(0, 1440)
            )
            accounts.append(
                Account(
                    account_id=f"act_{random.randint(100000, 999999)}",
                    type=random.choice(types),
                    seller=random.choice(SELLERS),
                    department=random.choice(departments),
                    status=status,
                    created_at=created,
                )
            )

        created_accounts = Account.objects.bulk_create(accounts)
        # bulk_create bypasses auto_now_add, so backfill the varied dates.
        for account in created_accounts:
            Account.objects.filter(pk=account.pk).update(created_at=account.created_at)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_accounts)} accounts."))
