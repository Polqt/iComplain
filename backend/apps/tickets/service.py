from __future__ import annotations

from typing import Iterable

from django.db import transaction

from .models import Ticket, TicketAttachment, TicketComment, TicketFeedback
from .validation import validate_file


def validate_attachments(attachments: Iterable) -> None:
    for uploaded in attachments or []:
        validate_file(uploaded)


def create_ticket_with_attachments(*, ticket_data, student, category, priority, attachments) -> Ticket:
    with transaction.atomic():
        ticket = Ticket.objects.create(
            title=ticket_data.title,
            description=ticket_data.description,
            student=student,
            category=category,
            priority=priority,
            building=ticket_data.building,
            room_name=ticket_data.room_name,
            status="pending",
        )
        for uploaded in attachments or []:
            TicketAttachment.objects.create(
                ticket=ticket,
                uploaded_by=student,
                file_path=uploaded,
                file_type=uploaded.content_type,
            )
    return ticket


def replace_ticket_attachments(*, ticket: Ticket, uploaded_by, attachments) -> None:
    with transaction.atomic():
        for existing in ticket.attachments_tickets.all():
            existing.file_path.delete(save=False)
            existing.delete()
        for uploaded in attachments or []:
            TicketAttachment.objects.create(
                ticket=ticket,
                uploaded_by=uploaded_by,
                file_path=uploaded,
                file_type=uploaded.content_type,
            )


def create_comment_with_attachments(*, ticket: Ticket, user, message: str, attachments) -> TicketComment:
    with transaction.atomic():
        comment = TicketComment.objects.create(
            ticket=ticket,
            user=user,
            message=message,
        )
        for uploaded in attachments or []:
            TicketAttachment.objects.create(
                comment=comment,
                uploaded_by=user,
                file_path=uploaded,
                file_type=uploaded.content_type,
            )
    return comment


def create_feedback_with_attachments(*, ticket: Ticket, student, rating: int, comments: str | None, attachments) -> TicketFeedback:
    with transaction.atomic():
        feedback = TicketFeedback.objects.create(
            ticket=ticket,
            student=student,
            rating=rating,
            comments=comments,
        )
        for uploaded in attachments or []:
            TicketAttachment.objects.create(
                feedback=feedback,
                uploaded_by=student,
                file_path=uploaded,
                file_type=uploaded.content_type,
            )
    return feedback
