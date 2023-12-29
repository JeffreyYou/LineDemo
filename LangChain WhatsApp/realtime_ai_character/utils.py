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
        logger.info(f'User {session_id} not found')
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


def handle_request(data):
    data = json.loads(data["text"])
    model = "gpt-4"
    temperature = 0
    message = data["message_content"]
    character = data["character"]
    operation = data["operation"]

    try:
        llm = get_llm(model, temperature, openai_api_key)
    except Exception as e:
        llm = None


    return llm, message, character, operation