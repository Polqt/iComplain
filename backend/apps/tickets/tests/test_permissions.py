import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.tickets.models import Category, Ticket, TicketPriority


User = get_user_model()


class TicketPermissionTests(TestCase):
    def setUp(self) -> None:
        password = "StrongPassword123!"
        self.student = User.objects.create_user(
            email="student@usls.edu.ph", password=password)
        self.other_student = User.objects.create_user(
            email="other@usls.edu.ph", password=password)
        self.admin = User.objects.create_user(
            email="admin@usls.edu.ph", password=password, is_staff=True)

        self.category = Category.objects.create(name="Plumbing")
        self.priority = TicketPriority.objects.create(
            name="Medium", level=2, color_code="#f59e0b")

        self.ticket = Ticket.objects.create(
            title="Leaky faucet",
            description="Faucet leaks continuously",
            student=self.student,
            category=self.category,
            priority=self.priority,
            building="Main",
            room_name="M105",
            status="pending",
        )

    def test_non_owner_cannot_delete_ticket(self) -> None:
        self.client.force_login(self.other_student)
        response = self.client.delete(f"/api/tickets/{self.ticket.id}")
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_pending_ticket(self) -> None:
        self.client.force_login(self.student)
        response = self.client.delete(f"/api/tickets/{self.ticket.id}")
        self.assertEqual(response.status_code, 204)

    def test_owner_cannot_delete_non_pending_ticket(self) -> None:
        self.ticket.status = "in_progress"
        self.ticket.save(update_fields=["status"])

        self.client.force_login(self.student)
        response = self.client.delete(f"/api/tickets/{self.ticket.id}")
        self.assertEqual(response.status_code, 400)

    def test_admin_can_update_any_ticket(self) -> None:
        self.client.force_login(self.admin)
        response = self.client.patch(
            f"/api/tickets/{self.ticket.id}/admin",
            data=json.dumps({"status": "in_progress"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_call_admin_patch(self) -> None:
        self.client.force_login(self.student)
        response = self.client.patch(
            f"/api/tickets/{self.ticket.id}/admin",
            data=json.dumps({"status": "resolved"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
