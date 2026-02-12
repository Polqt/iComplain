from pydantic import BaseModel
from datetime import datetime
from ninja import Schema

class UserSchema(BaseModel):
    id: int
    email: str
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
    class Config:
        from_attributes = True


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
    ticket: TicketSchema
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
    ticket: TicketSchema
    student: UserSchema
    rating: int
    comments: str | None = None
    created_at: datetime

class TicketFeedbackCreateSchema(Schema):
    rating: int
    comments: str | None = None

class TicketFeedbackUpdateSchema(Schema):
    rating: int | None = None
    comments: str | None = None
    