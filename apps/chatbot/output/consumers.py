import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from apps.chatbot.output.realtime_message_queue import RealtimeMessageQueryJobTask

# chat_channel = "chat"
chat_channel = "chat_channel"
logger = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # 获取 WebSocket 连接的房间名
        user_id = self.scope["path_remaining"][1:]

        # self.room_group_name = f"chat_{room_name}"
        # 接受 WebSocket 连接
        self.accept()

        # 将连接的客户端添加到特定频道
        # async_to_sync(self.channel_layer.group_add)(
        #     f"{chat_channel}_{user_id}",  # 设置频道名称
        #     self.channel_name
        # )
        async_to_sync(self.channel_layer.group_add)(
            chat_channel,  # 设置频道名称
            self.channel_name
        )
        logger.info(f'=> ws self : {user_id}，，，，')
        # RealtimeMessageQueryJobTask.start(user_id)
        logger.info(f'=> ws connect group : {chat_channel}')

    # 从特定频道中移除连接的客户端。
    def disconnect(self, close_code):
        # 在客户端断开连接时从频道中移除
        async_to_sync(self.channel_layer.group_discard)(
            chat_channel,  # 设置频道名称
            self.channel_name
        )

    # 方法在接收到客户端发送的消息时调用。
    # 目前被注释掉，因此不做任何处理。
    def receive(self, text_data):
        logger.info(f"=> run receive:{text_data}")
        # self.send(text_data=json.dumps({"message": text_data}))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        logger.info(f"=> run chat_message :{message}")
        text_data = json.dumps({"message": message})
        self.send(text_data=text_data)
