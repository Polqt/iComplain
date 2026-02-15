import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TicketNotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self):
        await self.channel_layer.group_add("ticket_updates", self.channel_name)
        await self.accept()
        
    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard("ticket_updates", self.channel_name)
        
    async def send_ticket_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))