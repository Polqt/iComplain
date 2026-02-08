from datetime import datetime
from ninja import Schema


class TicketSchema(Schema):
    id: int
    title: str
    description: str
    student: int
    category: int
    priority: int
    building: str
    room_name: str
    status: str
    created_at: datetime
    updated_at: datetime


class TicketCreateSchema(Schema):
    title: str
    description: str
    category: int
    priority: int
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
    updated_at: datetime 
    

class TicketAttachmentSchema(Schema):    
    id: int
    ticket: int
    uploaded_by: int
    file_path: str
    file_type: str
    uploaded_at: datetime


    
# COMMENT SCHEMA
     
class TicketCommentSchema(Schema):
    id: int
    ticket: int
    user: int
    message: str
    created_at: datetime

class TicketCommentCreateSchema(Schema):
    message: str
    
class TicketCommentUpdateSchema(Schema):
    message: str | None = None
    updated_at: datetime 

#Feedback Schema
class TicketFeedbackSchema(Schema):
    id: int
    ticket: int
    student: int
    rating: int
    comments: str | None = None
    created_at: datetime

class TicketFeedbackCreateSchema(Schema):
    rating: int
    comments: str | None = None

class TicketFeedbackUpdateSchema(Schema):
    rating: int | None = None
    comments: str | None = None
    updated_at: datetime 
