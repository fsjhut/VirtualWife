import json
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

        logger.error(f"environ:{os.environ}")
        self.OWN_API_URL = os.environ['OWN_API_URL']
        # self.OWN_API_URL = "http://192.168.123.234:8048/"

    def chat(self, prompt: str, role_name: str, you_name: str, query: str, short_history: list[dict[str, str]],
             long_history: str) -> str:
        pass
        # global result
        # global payload
        # prompt = prompt + query
        # logger.debug(f"prompt:{prompt}")
        # # 定义请求头
        # headers = {
        #     "Content-Type": "application/json",
        #     # 如果需要添加其他请求头，可以在这里添加
        # }
        # # 根据不同的接口地址，封装不同的请求参数
        # if self.OWN_API_URL.find("/chat/chat") != -1:
        #     # 定义请求体内容
        #     payload = {
        #         "query": query,
        #         "history": [
        #             {
        #                 "role": "user",
        #                 "content": "你好"
        #             },
        #             {
        #                 "role": "assistant",
        #                 "content": "你好，很高兴能为你提供帮助。"
        #             }
        #         ],
        #         "stream": True,
        #         "model_name": "Qwen-14B-Chat",
        #         "temperature": 0.7,
        #         "max_tokens": 0,
        #         "prompt_name": "default"
        #     }
        #
        # elif self.OWN_API_URL.find("/chat/search_engine_chat") != -1:
        #     pass
        #
        # elif self.OWN_API_URL.find("/chat/knowledge_base_chat") != -1:
        #     pass
        #
        # elif self.OWN_API_URL.find("/chat/agent_chat") != -1:
        #     pass
        #
        # elif self.OWN_API_URL.find("/chat/roleplay_chat") != -1:
        #     pass
        # else:
        #     payload = {"text": query}
        # json_payload = json.dumps(payload)
        # response = requests.post(self.OWN_API_URL, data=json_payload, headers=headers)
        # # 检查响应状态码
        # if response.status_code == 200:
        #     # 获取响应内容
        #     result = response.json()
        #     logger.info(result)
        # else:
        #     logger.error(f"请求失败，状态码：{response.status_code}")
        # return result

    async def chatStream(self,
                         prompt: str,
                         role_name: str,
                         you_name: str,
                         query: str,
                         history: list[dict[str, str]],
                         realtime_callback=None,
                         conversation_end_callback=None):
        logger.debug(f"prompt:{prompt}")
        global payload
        result_text = ""
        prompt = prompt + query
        logger.debug(f"prompt:{prompt}")
        # 定义请求头
        headers = {
            "Content-Type": "application/json",
            # 如果需要添加其他请求头，可以在这里添加
        }
        # 根据不同的接口地址，封装不同的请求参数
        if self.OWN_API_URL.find("/chat/chat") != -1:
            # 定义请求体内容
            payload = {
                "query": query,
                "history": self.format_history(history),
                "stream": "true",
                "model_name": "Qwen-14B-Chat",
                "temperature": 0.7,
                "max_tokens": 0,
                "prompt_name": "default"
            }
            json_payload = json.dumps(payload)
            response = requests.post(self.OWN_API_URL, data=json_payload, headers=headers)
            if response.status_code == 200:
                # 获取响应内容
                # 使用正则表达式提取text内容
                text_contents = re.findall(r'"text": "(.*?)"', response.text)
                # 拼接成新的字符串
                result_text = ''.join(text_contents)

        elif self.OWN_API_URL.find("/chat/search_engine_chat") != -1:
            pass

        elif self.OWN_API_URL.find("/chat/knowledge_base_chat") != -1:
            payload = {
                "query": query,
                "knowledge_base_name": "荣数测试数据",
                "top_k": 3,
                "score_threshold": 0.5,
                "history": self.format_history(history),
                "stream": "true",
                "model_name": "Qwen-14B-Chat",
                "temperature": 0.7,
                "max_tokens": 0,
                "prompt_name": "default"
            }
            json_payload = json.dumps(payload)
            response = requests.post(self.OWN_API_URL, data=json_payload, headers=headers)
            if response.status_code == 200:
                # 获取响应内容
                # 提取 "text" 属性
                text_contents = re.findall(r'"answer": "(.*?)"', response.text)
                result_text = ''.join(text_contents)
                result_text = re.sub(r'<[^>]+>', '', result_text)
                # 使用切片去掉末尾的字符
                result_text = result_text[:-1]

        elif self.OWN_API_URL.find("/chat/agent_chat") != -1:
            payload = {
                "query": "15的3次方是多少？",
                "history": self.format_history(history),
                "stream": "false",
                "model_name": "Qwen-14B-Chat",
                "temperature": 0.7,
                "max_tokens": 0,
                "prompt_name": "default"
            }
            json_payload = json.dumps(payload)
            response = requests.post(self.OWN_API_URL, data=json_payload, headers=headers)

        elif self.OWN_API_URL.find("/chat/roleplay_chat") != -1:
            payload = {
                "query": "15的3次方是多少？",
                "history": self.format_history(history),
                "model_name": "Qwen-14B-Chat",
                "temperature": 0.7,
                "max_tokens": 0,
                "roleplay_mode": "default",
                "details": ""
            }
            json_payload = json.dumps(payload)
            response = requests.post(self.OWN_API_URL, data=json_payload, headers=headers)
        else:
            payload = {"text": query}
            json_payload = json.dumps(payload)
            response = requests.post(self.OWN_API_URL, data=json_payload, headers=headers)
            if response.status_code == 200:
                # 获取响应内容
                # 提取 "text" 属性
                result = response.json()
                result = result['result']
                # 使用正则表达式去掉 HTML 标签
                result_text = re.sub(r'<[^>]+>', '', result)
        if result_text == "":
            logger.error(f"请求失败!")
        if realtime_callback:
            realtime_callback(role_name, 'own',
                              result_text, False)

    def format_history(self, history: list[dict[str, str]]):
        formatted_history = []
        for item in history:
            ai_temp = {
                "role": "assistant",
                "content": item.get('ai', ''),
            }
            user_temp = {
                "role": "user",
                "content": item.get('human', ''),
            }
            formatted_history.append(user_temp)
            formatted_history.append(ai_temp)
        # logger.info("formatted_history", formatted_history)
        return formatted_history
    # def format_history(self, history: list[dict[str, str]]):
    #     pass
