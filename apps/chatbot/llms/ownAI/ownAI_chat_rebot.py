import logging
import os
import re
from ...utils.str_utils import remove_spaces_and_tabs
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
import openai

logger = logging.getLogger(__name__)


class OwnAIGeneration():

    OWN_API_URL: str
    def __init__(self) -> None:
        from dotenv import load_dotenv
        load_dotenv()
        self.OWN_API_URL = "http://192.168.123.234:8048/"

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[dict[str, str]], long_history: str) -> str:
        global result
        prompt = prompt + query
        logger.debug(f"prompt:{prompt}")
        # 调用接口
        data_payload = {"text": query}
        response = requests.post(self.OWN_API_URL, json=data_payload)
        # 检查响应状态码
        if response.status_code == 200:
            # 获取响应内容
            result = response.json()
            logger.info(result)
        else:
            logger.error(f"请求失败，状态码：{response.status_code}")
        return result

    async def chatStream(self,
                         prompt: str,
                         role_name: str,
                         you_name: str,
                         query: str,
                         history: list[dict[str, str]],
                         realtime_callback=None,
                         conversation_end_callback=None):
        logger.debug(f"prompt:{prompt}")
        global result
        data_payload = {"text": query}
        response = requests.post(self.OWN_API_URL, json=data_payload)
        if response.status_code == 200:
            # 获取响应内容
            result = response.json()
            logger.info(result)
        else:
            logger.error(f"请求失败，状态码：{response.status_code}")
        result = result['result']
        # 使用正则表达式去掉 HTML 标签
        text_without_tags = re.sub(r'<[^>]+>', '', result)
        print(text_without_tags)
        if realtime_callback:
            realtime_callback(role_name, 'own',
                              text_without_tags, False)
