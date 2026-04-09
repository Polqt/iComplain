import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update an admin account from environment variables."

    def handle(self, *args, **kwargs):
        email = os.getenv("SEED_ADMIN_EMAIL", "").strip().lower()
        password = os.getenv("SEED_ADMIN_PASSWORD", "")
        full_name = os.getenv("SEED_ADMIN_FULL_NAME", "").strip()

        if not email and not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping admin seed: SEED_ADMIN_EMAIL and SEED_ADMIN_PASSWORD are not set."
                )
            )
            return

        if not email or not password:
            raise CommandError(
                "Both SEED_ADMIN_EMAIL and SEED_ADMIN_PASSWORD must be set together."
            )

        User = get_user_model()
        user, created = User.objects.get_or_create(email=email)
        changed = created

        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not getattr(user, "is_superuser", False):
            user.is_superuser = True
            changed = True
        if not user.is_active:
            user.is_active = True
            changed = True
        if full_name and getattr(user, "full_name", "") != full_name:
            user.full_name = full_name
            changed = True

        # Keep password in sync with the configured seed credentials.
        user.set_password(password)
        changed = True

        if changed:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created admin account: {email}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated admin account: {email}"))
