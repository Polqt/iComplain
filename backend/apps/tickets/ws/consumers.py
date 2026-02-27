import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TicketNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        # Join the global ticket updates group
        await self.channel_layer.group_add("ticket_updates", self.channel_name)
        
        # Join user-specific group for per-user notifications (e.g. status changes, comments)
        self.user_group = f"user_{user.id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("ticket_updates", self.channel_name)
        
        if getattr(self, "user_group", None):
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