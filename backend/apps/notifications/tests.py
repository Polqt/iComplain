import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.notifications.models import InAppNotification
from apps.tickets.models import Category, Ticket, TicketPriority


User = get_user_model()


class NotificationsApiTests(TestCase):
    def setUp(self) -> None:
        self.password = "StrongPassword123!"
        self.student = User.objects.create_user(
            email="student@usls.edu.ph",
            password=self.password,
        )
        self.staff = User.objects.create_user(
            email="admin@usls.edu.ph",
            password=self.password,
            is_staff=True,
        )

        self.category = Category.objects.create(name="Electrical")
        self.priority = TicketPriority.objects.create(
            name="Medium",
            level=2,
            color_code="#f59e0b",
        )
        self.ticket = Ticket.objects.create(
            title="Flickering lights",
            description="Room lights keep flickering.",
            student=self.student,
            category=self.category,
            priority=self.priority,
            building="Main",
            room_name="M101",
        )

    def test_requires_auth_for_inapp_list(self) -> None:
        response = self.client.get("/api/notifications/inapp/")

        self.assertEqual(response.status_code, 401)

    def test_list_inapp_notifications_for_authenticated_user(self) -> None:
        InAppNotification.objects.create(
            user=self.student,
            ticket=self.ticket,
            event="ticket_created",
            title="New ticket",
            message="Ticket created",
            notification_type="info",
        )

        self.client.force_login(self.student)
        response = self.client.get("/api/notifications/inapp/?limit=10")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "New ticket")

    def test_mark_notification_read(self) -> None:
        n = InAppNotification.objects.create(
            user=self.student,
            ticket=self.ticket,
            event="ticket_updated",
            title="Updated",
            message="Updated",
            notification_type="info",
        )
        self.client.force_login(self.student)

        response = self.client.patch(
            f"/api/notifications/inapp/{n.id}/",
            data=json.dumps({"read": True}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        n.refresh_from_db()
        self.assertTrue(n.read)

    def test_mark_all_read(self) -> None:
        InAppNotification.objects.create(
            user=self.student,
            ticket=self.ticket,
            event="ticket_created",
            title="A",
            message="A",
            notification_type="info",
            read=False,
        )
        InAppNotification.objects.create(
            user=self.student,
            ticket=self.ticket,
            event="ticket_updated",
            title="B",
            message="B",
            notification_type="info",
            read=False,
        )
        self.client.force_login(self.student)

        response = self.client.post("/api/notifications/inapp/mark-all-read/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["marked"], 2)
        self.assertEqual(
            InAppNotification.objects.filter(
                user=self.student, read=False).count(),
            0,
        )

    def test_only_staff_can_create_email_notification(self) -> None:
        self.client.force_login(self.student)
        response = self.client.post(
            "/api/notifications/",
            data=json.dumps(
                {
                    "user": self.student.id,
                    "ticket": self.ticket.id,
                    "event": "CREATED",
                    "status": "SENT",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.staff)
        response = self.client.post(
            "/api/notifications/",
            data=json.dumps(
                {
                    "user": self.student.id,
                    "ticket": self.ticket.id,
                    "event": "CREATED",
                    "status": "SENT",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
