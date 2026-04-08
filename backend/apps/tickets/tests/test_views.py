import json

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart

from apps.tickets.models import Category, Ticket, TicketAttachment, TicketPriority


User = get_user_model()


class TicketViewsApiTests(TestCase):
    def setUp(self) -> None:
        self.password = "StrongPassword123!"
        self.student = User.objects.create_user(
            email="student@usls.edu.ph",
            password=self.password,
        )
        self.other_student = User.objects.create_user(
            email="other@usls.edu.ph",
            password=self.password,
        )
        self.admin = User.objects.create_user(
            email="admin@usls.edu.ph",
            password=self.password,
            is_staff=True,
        )

        self.category = Category.objects.create(name="Electrical")
        self.priority_low = TicketPriority.objects.create(
            name="Low", level=1, color_code="#10b981"
        )
        self.priority_medium = TicketPriority.objects.create(
            name="Medium", level=2, color_code="#f59e0b"
        )

    def _login(self, user) -> None:
        self.client.force_login(user)

    def _create_ticket(self, owner=None, status="pending") -> Ticket:
        owner = owner or self.student
        return Ticket.objects.create(
            title="Projector not working",
            description="Projector in room is black screen.",
            student=owner,
            category=self.category,
            priority=self.priority_medium,
            building="Main",
            room_name="M204",
            status=status,
        )

    def test_student_ticket_lifecycle_create_update_delete(self) -> None:
        self._login(self.student)

        create_response = self.client.post(
            "/api/tickets/",
            data={
                "title": "Broken chair",
                "description": "Chair leg is loose",
                "category": str(self.category.id),
                "building": "Main",
                "room_name": "M102",
            },
        )
        self.assertEqual(create_response.status_code, 200)
        created = create_response.json()
        ticket_id = created["id"]

        update_payload = encode_multipart(
            BOUNDARY,
            {
                "title": "Broken chair updated",
                "description": "Chair still broken",
                "category": str(self.category.id),
                "building": "Main",
                "room_name": "M103",
                "status": "pending",
            },
        )
        update_response = self.client.generic(
            "PUT",
            f"/api/tickets/{ticket_id}",
            update_payload,
            content_type=MULTIPART_CONTENT,
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()[
                         "title"], "Broken chair updated")

        delete_response = self.client.delete(f"/api/tickets/{ticket_id}")
        self.assertEqual(delete_response.status_code, 204)

        self.assertTrue(
            Ticket.objects.filter(
                id=ticket_id, archived_at__isnull=False).exists()
        )

    def test_student_cannot_edit_non_pending_ticket(self) -> None:
        ticket = self._create_ticket(status="in_progress")
        self._login(self.student)

        response = self.client.put(
            f"/api/tickets/{ticket.id}",
            data={
                "title": "Try edit",
                "description": ticket.description,
                "category": str(self.category.id),
                "building": ticket.building,
                "room_name": ticket.room_name,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_student_cannot_edit_other_students_ticket(self) -> None:
        ticket = self._create_ticket(owner=self.other_student)
        self._login(self.student)

        response = self.client.put(
            f"/api/tickets/{ticket.id}",
            data={
                "title": "No permission",
                "description": ticket.description,
                "category": str(self.category.id),
                "building": ticket.building,
                "room_name": ticket.room_name,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_patch_status_and_priority(self) -> None:
        ticket = self._create_ticket(status="pending")
        self._login(self.admin)

        response = self.client.patch(
            f"/api/tickets/{ticket.id}/admin",
            data=json.dumps(
                {"status": "resolved", "priority": self.priority_low.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "resolved")
        self.assertEqual(ticket.priority_id, self.priority_low.id)

    def test_feedback_lifecycle_requires_resolved_then_closes_ticket(self) -> None:
        ticket = self._create_ticket(status="resolved")
        self._login(self.student)

        create_response = self.client.post(
            f"/api/tickets/{ticket.id}/feedback/",
            data={"rating": "5", "comments": "Great job"},
        )
        self.assertEqual(create_response.status_code, 201)

        feedback_id = create_response.json()["id"]
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "closed")

        update_response = self.client.put(
            f"/api/tickets/{ticket.id}/feedback/{feedback_id}",
            data=json.dumps({"comments": "Updated comment", "rating": 4}),
            content_type="application/json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["rating"], 4)

    def test_feedback_forbidden_for_non_owner(self) -> None:
        ticket = self._create_ticket(
            status="resolved", owner=self.other_student)
        self._login(self.student)

        response = self.client.post(
            f"/api/tickets/{ticket.id}/feedback/",
            data={"rating": "5", "comments": "Not owner"},
        )

        self.assertEqual(response.status_code, 403)

    def test_comment_upload_accepts_no_file(self) -> None:
        ticket = self._create_ticket(status="pending")
        self._login(self.student)

        response = self.client.post(
            f"/api/tickets/{ticket.id}/comments",
            data={"message": "No file"},
        )

        self.assertEqual(response.status_code, 200)

    def test_comment_upload_accepts_one_valid_file(self) -> None:
        ticket = self._create_ticket(status="pending")
        self._login(self.student)

        png_bytes = (
            b"\x89PNG\r\n\x1a\n"
            b"\x00\x00\x00\rIHDR"
            b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00"
            b"\x90wS\xde\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
            b"\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        upload = SimpleUploadedFile(
            "proof.png", png_bytes, content_type="image/png")

        response = self.client.post(
            f"/api/tickets/{ticket.id}/comments",
            data={"message": "With one file", "attachment": upload},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TicketAttachment.objects.filter(
            comment_id=response.json()["id"]).count(), 1)

    def test_comment_upload_accepts_multiple_valid_files(self) -> None:
        ticket = self._create_ticket(status="pending")
        self._login(self.student)

        png_1 = (
            b"\x89PNG\r\n\x1a\n"
            b"\x00\x00\x00\rIHDR"
            b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00"
            b"\x90wS\xde\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
            b"\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        png_2 = png_1
        file_1 = SimpleUploadedFile("a.png", png_1, content_type="image/png")
        file_2 = SimpleUploadedFile("b.png", png_2, content_type="image/png")

        response = self.client.post(
            f"/api/tickets/{ticket.id}/comments",
            data={"message": "With multiple files",
                  "attachment": [file_1, file_2]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TicketAttachment.objects.filter(
            comment_id=response.json()["id"]).count(), 2)

    def test_comment_upload_rejects_invalid_type(self) -> None:
        ticket = self._create_ticket(status="pending")
        self._login(self.student)

        bad = SimpleUploadedFile(
            "bad.exe", b"MZ\x00\x00not-an-image", content_type="application/x-msdownload")

        response = self.client.post(
            f"/api/tickets/{ticket.id}/comments",
            data={"message": "Bad type", "attachment": bad},
        )

        self.assertEqual(response.status_code, 400)

    def test_comment_upload_rejects_oversized_file(self) -> None:
        ticket = self._create_ticket(status="pending")
        self._login(self.student)

        big_content = b"%PDF-" + b"x" * (5 * 1024 * 1024 + 1024)
        big = SimpleUploadedFile(
            "big.pdf", big_content, content_type="application/pdf")

        response = self.client.post(
            f"/api/tickets/{ticket.id}/comments",
            data={"message": "Too big", "attachment": big},
        )

        self.assertEqual(response.status_code, 400)

    def test_end_to_end_student_admin_feedback_flow(self) -> None:
        self._login(self.student)

        create_response = self.client.post(
            "/api/tickets/",
            data={
                "title": "Broken outlet",
                "description": "Outlet sparks intermittently",
                "category": str(self.category.id),
                "building": "Main",
                "room_name": "M110",
            },
        )
        self.assertEqual(create_response.status_code, 200)
        ticket_id = create_response.json()["id"]

        self.client.force_login(self.admin)
        admin_response = self.client.patch(
            f"/api/tickets/{ticket_id}/admin",
            data=json.dumps(
                {"status": "resolved", "priority": self.priority_low.id}),
            content_type="application/json",
        )
        self.assertEqual(admin_response.status_code, 200)

        self.client.force_login(self.student)
        feedback_response = self.client.post(
            f"/api/tickets/{ticket_id}/feedback/",
            data={"rating": "5", "comments": "Resolved quickly"},
        )
        self.assertEqual(feedback_response.status_code, 201)

        ticket = Ticket.objects.get(id=ticket_id)
        self.assertEqual(ticket.status, "closed")
