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


class InAppNotificationSchema(Schema):
    id: str 
    type: str 
    title: str
    message: str
    timestamp: str  # ISO or formatted
    read: bool
    actionUrl: str | None = None
    actionLabel: str | None = None


class InAppNotificationMarkReadSchema(Schema):
    read: bool = True