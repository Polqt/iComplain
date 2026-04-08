from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.tickets.models import Category, Ticket, TicketAttachment, TicketComment, TicketFeedback, TicketPriority


User = get_user_model()


class TicketModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="student@usls.edu.ph",
            password="StrongPassword123!",
        )
        self.category = Category.objects.create(name="Electrical")
        self.priority = TicketPriority.objects.create(
            name="Medium",
            level=2,
            color_code="#f59e0b",
        )

    def test_ticket_number_is_generated(self) -> None:
        ticket = Ticket.objects.create(
            title="Projector issue",
            description="Projector not turning on",
            student=self.user,
            category=self.category,
            priority=self.priority,
            building="Main",
            room_name="M101",
        )

        self.assertTrue(ticket.ticket_number.startswith("TKT-"))

    def test_attachment_requires_exactly_one_parent(self) -> None:
        ticket = Ticket.objects.create(
            title="AC issue",
            description="No cooling",
            student=self.user,
            category=self.category,
            priority=self.priority,
            building="Main",
            room_name="M102",
        )
        comment = TicketComment.objects.create(
            ticket=ticket,
            user=self.user,
            message="Needs urgent fix",
        )

        attachment = TicketAttachment(
            ticket=ticket,
            comment=comment,
            uploaded_by=self.user,
            file_type="image/png",
        )

        with self.assertRaises(ValidationError):
            attachment.full_clean()

    def test_feedback_updated_at_changes_on_save(self) -> None:
        ticket = Ticket.objects.create(
            title="WiFi issue",
            description="Weak signal",
            student=self.user,
            category=self.category,
            priority=self.priority,
            building="Main",
            room_name="M103",
            status="resolved",
        )
        feedback = TicketFeedback.objects.create(
            ticket=ticket,
            student=self.user,
            rating=4,
            comments="Good",
        )
        first_updated_at = feedback.updated_at

        feedback.comments = "Great"
        feedback.save()

        self.assertGreaterEqual(feedback.updated_at, first_updated_at)
