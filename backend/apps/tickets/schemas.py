from typing import List, Optional, Literal
from pydantic import BaseModel
from datetime import datetime
from ninja import Schema

class UserSchema(BaseModel):
    id: int
    email: str
    name: str | None = None
    avatar: str | None = None
    class Config:
        from_attributes = True

class CategorySchema(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True


class TicketPrioritySchema(BaseModel):
    id: int
    name: str
    level: int
    color_code: str
    class Config:
        from_attributes = True


class TicketSchema(BaseModel):
    id: int
    title: str
    description: str
    student: UserSchema
    category: CategorySchema
    priority: TicketPrioritySchema
    building: str
    room_name: str
    status: str
    created_at: datetime
    updated_at: datetime
    ticket_number: str
    attachment: Optional[str] = None
    comments_count: int = 0
    has_feedback: bool = False
    
    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, ticket, request=None):
        attachment_url = None
        first = getattr(ticket, 'attachments_tickets', None)
        if first and hasattr(first, 'first'):
            first_attachment = first.first()
            if first_attachment:
                relative = first_attachment.file_path.url
                if request is not None:
                    attachment_url = request.build_absolute_uri(relative)
                else:
                    attachment_url = relative
                    
        has_feedback = False
        try:
            has_feedback = bool(ticket.feedback)
        except AttributeError:
            has_feedback = False
        
        data = {
            "id":            ticket.id,
            "title":         ticket.title,
            "description":   ticket.description,
            "student":       ticket.student,
            "category":      ticket.category,
            "priority":      ticket.priority,
            "building":      ticket.building,
            "room_name":     ticket.room_name,
            "status":        ticket.status,
            "created_at":    ticket.created_at,
            "updated_at":    ticket.updated_at,
            "ticket_number": ticket.ticket_number,
            "attachment":    attachment_url,
            "comments_count": getattr(ticket, 'comments_count', 0),
            "has_feedback":  has_feedback
        }
        return cls.model_validate(data)


class TicketCreateSchema(Schema):
    title: str
    description: str
    category: int
    building: str
    room_name: str

class TicketUpdateSchema(Schema):
    title: str | None = None
    description: str | None = None
    category: int | None = None
    priority: int | None = None
    building: str | None = None
    room_name: str | None = None
    status: str | None = None

class TicketAdminUpdateSchema(Schema):
    status: str | None = None
    priority: int | None = None
    

class TicketAttachmentSchema(Schema):    
    id: int
    ticket: int
    uploaded_by: int
    file_path: str
    file_type: str
    uploaded_at: datetime


# COMMENT SCHEMA
     
class TicketCommentSchema(BaseModel):
    id: int
    ticket_id: int
    user: UserSchema
    message: str
    created_at: datetime
    class Config:
        from_attributes = True


class TicketCommentCreateSchema(Schema):
    message: str
    
class TicketCommentUpdateSchema(Schema):
    message: str | None = None


#Feedback Schema
class TicketFeedbackSchema(Schema):
    id: int
    ticket_id: int
    student: UserSchema
    rating: int
    comments: str | None = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, feedback):
        data = {
                "id": feedback.id,
                "ticket_id": feedback.ticket.id if hasattr(feedback, 'ticket') else None,
                "student": feedback.student,
                "rating": feedback.rating,
                "comments": feedback.comments,
                "created_at": feedback.created_at,
                "updated_at": getattr(feedback, 'updated_at', feedback.created_at),
            }
        return cls.model_validate(data)

class TicketFeedbackCreateSchema(Schema):
    rating: int
    comments: str | None = None

class TicketFeedbackUpdateSchema(Schema):
    rating: int | None = None
    comments: str | None = None


class TicketHistoryItemSchema(Schema):
    id: str
    ticketPk: int
    ticketId: str
    title: str
    action: Literal["created", "updated", "resolved", "closed", "commented", "reopened"]
    description: str
    timestamp: str
    date: str
    status: Literal["pending", "in-progress", "resolved", "closed"]
    priority: Literal["low", "medium", "high"]
    category: str | None = None
    performedBy: str | None = None

class DashboardMetricsSchema(Schema):
    title: str
    value: str
    change: str
    subtitle: str
    trend: str
    is_critical: bool = False  # For pending/urgent metrics that need visual emphasis
    is_increasing: bool = False  # Direction of change (for trend arrow display)
    
class TicketVolumeDataPointSchema(Schema):
    day: str
    value: int
    
class DashboardStatsSchema(Schema):
    metrics: list[DashboardMetricsSchema]
    volume: list[TicketVolumeDataPointSchema]
    status_breakdown: dict[str, int]
    category_breakdown: dict[str, int]
    recent_activity: list[dict] | None = None  # For activity feed

class ActivityLogSchema(Schema):
    """Schema for activity log entries."""
    id: int
    action: Literal["created", "status_changed", "priority_changed", "assigned", "commented", "reopened", "resolved"]
    ticket_number: str
    ticket_title: str
    performed_by: UserSchema | None
    description: str
    old_value: str | None = None
    new_value: str | None = None
    created_at: datetime
    
    @classmethod
    def from_orm(cls, activity_log):
        """Custom ORM mapping to extract ticket details from related FK."""
        performed_by_data = None
        if activity_log.performed_by:
            performed_by_data = {
                'id': activity_log.performed_by.id,
                'email': activity_log.performed_by.email,
                'name': getattr(activity_log.performed_by, 'name', None),
                'avatar': getattr(activity_log.performed_by, 'avatar', None),
            }
        
        data = {
            'id': activity_log.id,
            'action': activity_log.action,
            'ticket_number': activity_log.ticket.ticket_number,
            'ticket_title': activity_log.ticket.title,
            'performed_by': performed_by_data,
            'description': activity_log.description,
            'old_value': activity_log.old_value,
            'new_value': activity_log.new_value,
            'created_at': activity_log.created_at,
        }
        return cls.model_validate(data)


class ActivityLogListSchema(Schema):
    """Paginated activity log response."""
    items: list[ActivityLogSchema]
    total: int
    limit: int
    offset: int