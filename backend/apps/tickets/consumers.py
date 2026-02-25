import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TicketNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the global ticket updates group
        await self.channel_layer.group_add("ticket_updates", self.channel_name)
        await self.channel_layer.group_add("comment_updates", self.channel_name)
        await self.channel_layer.group_add("feedback_updates", self.channel_name)

        # Join user-specific group for per-user notifications (e.g. status changes, comments)
        user = self.scope.get("user")
        if user and user.is_authenticated:
            self.user_group = f"user_{user.id}"
            await self.channel_layer.group_add(self.user_group, self.channel_name)
        else:
            self.user_group = None

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("ticket_updates", self.channel_name)
        await self.channel_layer.group_discard("comment_updates", self.channel_name)
        await self.channel_layer.group_discard("feedback_updates", self.channel_name)
        if self.user_group:
            await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def send_ticket_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def send_comment_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def send_feedback_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def send_status_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))