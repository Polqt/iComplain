from ninja import Schema


class EmailNotificationSchema(Schema):
    id: int
    user: int
    ticket: int
    event: str
    sent_at: str
    status: str

class EmailNotificationCreateSchema(Schema):
    user: int
    ticket: int
    event: str
    status: str