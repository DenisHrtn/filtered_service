import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filtering_service.settings')

import django
django.setup()

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models.user_data import UserData


class SendUserDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.is_active = True

    async def disconnect(self, code):
        self.is_active = False
        print(f"Client disconnected with code: {code}")
        await sync_to_async(self.log_disconnect)(code)

    def log_disconnect(self, code):
        with open('sockets_logs.log', 'w', encoding='utf-8') as file:
            file.write(f"Client disconnected with code: {code}")

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        command = data.get('command', None)

        if command == 'start sending user data':
            user_data_list = await sync_to_async(list)(UserData.objects.all())

            for user_data in user_data_list:
                if not self.is_active:
                    print("Client has disconnected, stopping the data send!")
                    break

                user_data_dict = {
                    'email': user_data.email,
                    'name': user_data.name,
                    'surname': user_data.surname,
                    'patronymic': user_data.patronymic,
                    'birth_date': str(user_data.birth_date),
                    'gender': user_data.gender,
                    'phone_number': user_data.phone_number,
                    'age': user_data.age,
                    'user_id': user_data.user_id,
                    'login': user_data.login,
                    'timestamp': user_data.timestamp,
                    'support_level': user_data.support_level,
                    'message': user_data.message
                }

                await self.send(text_data=json.dumps(user_data_dict))

                await asyncio.sleep(5)