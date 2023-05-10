import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VacancyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.vacancy_id = self.scope['url_route']['kwargs']['vacancy_id']
        self.vacancy_group_name = f'vacancy_{self.vacancy_id}'

        await self.channel_layer.group_add(
            self.vacancy_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.vacancy_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.vacancy_group_name,
            {
                'type': 'vacancy_notification',
                'message': message
            }
        )

    async def vacancy_notification(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
