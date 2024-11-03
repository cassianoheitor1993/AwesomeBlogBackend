# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        # log the event
        print("NotificationConsumer event: ", event)
        message = event['message']
        article_name = event.get('article_name', 'Unknown')
        article_date = event.get('article_date', 'Unknown')
        article_author = event.get('article_author', 'Unknown')
        article_link = event.get('article_link', 'Unknown')

        await self.send(text_data=json.dumps({
            'message': message,
            'article_name': article_name,
            'article_date': article_date,
            'article_author': article_author,
            'article_link': article_link
        }))