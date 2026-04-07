from django.core.management.base import BaseCommand
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'List all admin accounts and reset password'

    def handle(self, *args, **kwargs):
        admins = CustomUser.objects.filter(is_staff=True)
        if not admins.exists():
            self.stdout.write(self.style.WARNING('No admin accounts found.'))
            return

        self.stdout.write(self.style.SUCCESS('=== Admin Accounts ==='))
        for user in admins:
            self.stdout.write(f'  Email: {user.email} | Name: {user.full_name} | Superuser: {user.is_superuser}')

        # Reset password for first admin found
        first_admin = admins.first()
        new_password = 'Admin@iComplain2024'
        first_admin.set_password(new_password)
        first_admin.save()
        self.stdout.write(self.style.SUCCESS(f'\nPassword reset for {first_admin.email} → {new_password}'))
