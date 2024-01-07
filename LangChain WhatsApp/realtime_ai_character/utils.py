from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic.dataclasses import dataclass
from typing import List, Optional, Callable
from dataclasses import field
from starlette.websockets import WebSocket, WebSocketState
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from realtime_ai_character.models.interaction import Interaction
from realtime_ai_character.models.user import User
from realtime_ai_character.llm.openai_llm import get_llm, AsyncCallbackTextHandler
from sqlalchemy import and_

import os
import json
import asyncio
import re
import base64
import requests

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

@dataclass
class Character:
    character_id: str
    name: str
    llm_system_prompt: str
    llm_user_prompt: str
    source: str = ''
    location: str = ''
    voice_id: str = ''
    author_name: str = ''
    author_id: str = ''
    avatar_id: Optional[str] = ''
    visibility: str = ''
    tts: Optional[str] = ''
    data: Optional[dict] = None
    notification: str = ''

@dataclass
class ConversationHistory:
    system_prompt: str = ''
    user: list[str] = field(default_factory=list)
    ai: list[str] = field(default_factory=list)

    def __iter__(self):
        yield self.system_prompt
        for user_message, ai_message in zip(self.user, self.ai):
            yield user_message
            yield ai_message
    def __str__(self):
        return f"System: {self.system_prompt}, user: {self.user}, ai: {self.ai}"
    def load_from_db(self, session_id: str, character_name: str, db: Session):
        conversations = db.query(Interaction).filter(and_(Interaction.session_id == session_id, Interaction.character_name == character_name)).order_by(Interaction.timestamp).all()
        for conversation in conversations:
            self.user.append(conversation.client_message_unicode)
            self.ai.append(conversation.server_message_unicode)


class Singleton:
    _instances = {}

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """ Static access method. """
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)

        return cls._instances[cls]

    @classmethod
    def initialize(cls, *args, **kwargs):
        """ Static access method. """
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)


def build_history(conversation_history: ConversationHistory) -> List[BaseMessage]:
    history = []
    for i, message in enumerate(conversation_history):
        if i == 0:
            history.append(SystemMessage(content=message))
        elif i % 2 == 0:
            history.append(AIMessage(content=message))
        else:
            history.append(HumanMessage(content=message))
    return history
def build_history_image(conversation_history: ConversationHistory, system_prompt) -> List[BaseMessage]:
    history = []
    for i, message in enumerate(conversation_history):
        if i == 0:
            history.append(SystemMessage(content=system_prompt))
        elif i % 2 == 0:
            history.append(AIMessage(content=message))
        else:
            history.append(HumanMessage(content=message))
    return history


class ConnectionManager(Singleton):
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client #{id(websocket)} left the chat")
        # await self.broadcast_message(f"Client #{id(websocket)} left the chat")

    async def send_message(self, message: str, websocket: WebSocket):
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.send_text(message)

    async def broadcast_message(self, message: str):
        for connection in self.active_connections:
            if connection.application_state == WebSocketState.CONNECTED:
                await connection.send_text(message)


def get_connection_manager():
    return ConnectionManager.get_instance()

@dataclass
class SessionAuthResult:
    is_existing_session: bool
    is_authenticated_user: bool

# @dataclass
# class UserAuthResult:
#     is_user_exist: bool
#     user_id: str
#     user_name: str
#     investment_knowledge: str
#     is_open_account: bool
#     account_agency: str
#     is_in_group: bool
@dataclass
class UserAuthResult:
    is_user_exist: bool


async def check_session_auth(session_id: str, character_name: str, db: Session, logger) -> SessionAuthResult:
    try:
        original_chat = await asyncio.to_thread(
            db.query(Interaction).filter(and_(Interaction.session_id == session_id, Interaction.character_name == character_name)).first)
    except Exception as e:
        logger.info(f'Failed to lookup session {session_id} with error {e}')
        return SessionAuthResult(
            is_existing_session=False,
            is_authenticated_user=False,
        )
    if not original_chat:
        return SessionAuthResult(
            is_existing_session=False,
            is_authenticated_user=False,
        )
    return SessionAuthResult(
            is_existing_session=True,
            is_authenticated_user=False,
    )
async def check_user_info(session_id: str, db: Session, logger) -> UserAuthResult:
    try:
        user_info = await asyncio.to_thread(
            db.query(User).filter(User.user_id == session_id).first
        )
    except Exception as e:
        logger.info(f'User {session_id} Error: {e}')
        return UserAuthResult(
            is_user_exist=False,
        )
    if user_info:
            return user_info
    else:
        logger.info(f'User {session_id} doesn\'t have user infomation')
        return None
    
async def load_user_info(session_id: str, db: Session, logger):
    try:
        user_info = await asyncio.to_thread(
            db.query(User).filter(User.user_id == session_id).first)
        return user_info
    except Exception as e:
        logger.info(f'User {session_id} info not available since {e}')
        return None

def delete_chat_history(character_name: str, session_id: str, db: Session):
    records = db.query(Interaction).filter(and_(Interaction.session_id == session_id, Interaction.character_name == character_name)).all()
    if records:
        for record in records:
            db.delete(record)
def delete_user_history(user_id: str, db: Session):
    records = db.query(User).filter(User.user_id == user_id).all()
    if records:
        for record in records:
            db.delete(record)

def handle_request(data):
    data = json.loads(data["text"])
    model = "gpt-4-1106-preview"
    temperature = 0
    message = data["message_content"]
    character = data["character"]
    operation = data["operation"]

    try:
        llm = get_llm(model, temperature, openai_api_key)
    except Exception as e:
        llm = None


    return llm, message, character, operation
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f
def handle_request_image(data, session_id, image_map):
    # path = 'C:\\Users\\nickd\\Desktop\\test'
    # for img in findAllFile(path):
    #     image_path = path + '/' + img
    #     base64_image = encode_image(image_path)
    data = json.loads(data["text"])
    url = data["message_content"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": 
                """
                    你的職責
                    ###
                    請讀取這張圖片的內容，並根據其內容按照"Json模板生成答案"
                    不管是不清楚還是沒有的讀取到的的內容都用 "None" 代替
                    ###
                    Json模板
                    ###
                    {   
                        isInvestment: 是否為證券交易截圖 (yes or no)
                        descriptionIfNot: 如果不是證券交易截圖,描述這個圖片
                        pictureInfo: {
                            顯示時間: ,
                            網頁標題: ,
                            公司類型: ,
                            橫幅: {
                                是否有橫幅: (yes or no),
                                橫幅內容: ,
                                橫幅含義: 
                            },
                            股票交易詳情，從表格裏獲得相關內容，多少株就是多少股的成交數量，HKD就是成交單價: {
                            註文番號: 一般是類似0007這種格式和註文日時附近,
                            內容:  ,
                            銘柄: 一般都是06918類似這種格式，在標題是 銘柄的列表裏
                            註文數量:  xxx株，從註文數量裏獲得  假設識別20.000不是20株，是2萬株的意思，當後面是000的時候，說明是,而不是.
                            註文單價:  xxxHKD，一般都是类似1.720HKD,不会有逗号出现，只有小数点
                            成交日期:  ,
                            結算日期:  ,
                            合計金額:  ,
                            手續費:  ,
                            成交時間:  
                            },
                            底部: {
                                是否有註釋: (yes or no),
                                註釋內容:  ,
                                是否有網址: (yes or no),
                                網址內容:  
                            }
                        }
                    }
                    ###
                """
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": url
                }
                }
            ]
            }
        ],
        "max_tokens": 500
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    res = response.json()['choices'][0]['message']['content']
    print(res)
    image_map[session_id] = res
    return res

async def chaining_user_info(session_id: str, db: Session, logger, conversation_history, catalog_manager, llm, on_new_token_null):
    user_auth = await check_user_info(session_id, db, logger)
    if user_auth:
        logger.info(f"User #{session_id} is loading UserInfo from existing session")
        user_info = await load_user_info(session_id, db, logger)
        conversation_history.system_prompt += f'''
        用户信息:
        ###
        用户姓名:{user_info.user_name}
        ###
        '''.strip()
    else:
        logger.info(f"User {session_id}: generating user profile...")
        user_conversation = ConversationHistory()
        analysis_character = catalog_manager.get_character("UserAnalysis")
        user_conversation.system_prompt = analysis_character.llm_system_prompt

        await asyncio.to_thread(user_conversation.load_from_db, session_id=session_id, character_name="DemoDay01" , db=db)
        user_info_response = await llm.achat(
            history = build_history(user_conversation),
            user_input = "",
            user_input_template = analysis_character.llm_user_prompt,
            callback = AsyncCallbackTextHandler(on_new_token_null)
        )

        user_info_response = json.loads(user_info_response)
        user = User(user_id = session_id,
                    user_name = user_info_response["name"],
                    investment_knowledge = user_info_response["investment_knowledge"],
                    account_agency = user_info_response["account_agency"],
                    is_in_group = user_info_response["is_in_group"] == "yes",
                    is_open_account = user_info_response["is_open_account"] == "yes"
                    )
        user_info_rga =  f'''\n用户信息:\n###\n'''
        user_info_rga += f'用户姓名: {user_info_response["name"]}\n'.strip()
        user_info_rga += '###\n'
        conversation_history.system_prompt += user_info_rga
        await asyncio.to_thread(user.save, db) 

def chaining_question_rag(catalog_manager, conversation_history, message, logger):
    logger.info(f"Retrieving similar questios: {message}")

    chroma = catalog_manager.get_chroma()
    docs =chroma.similarity_search(message, 2)
    rga_info = []
    for doc in docs:
        chats = re.findall(r'\[([^\]]+)\]', doc.page_content)
        for chat in chats:
            rga_info.append(chat.strip())
    rga_content = f'''\n补充信息\n###\n'''
    for rga in rga_info:
        rga_content += f'{rga}\n'
    rga_content += '###\n'
    conversation_history.system_prompt += rga_content

def chaining_picture_rag(conversation_history, session_id, image_map):
    if session_id in image_map:
        conversation_history.system_prompt += """用户交易信息\n###\n"""
        conversation_history.system_prompt += image_map[session_id]
        conversation_history.system_prompt += """\n###"""


    
