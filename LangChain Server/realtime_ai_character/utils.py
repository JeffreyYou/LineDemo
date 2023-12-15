from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic.dataclasses import dataclass
from typing import List, Optional, Callable
from dataclasses import field
from starlette.websockets import WebSocket, WebSocketState
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from realtime_ai_character.models.interaction import Interaction

import os
import json
from realtime_ai_character.llm.openai_llm import get_llm, AsyncCallbackTextHandler

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
    def load_from_db(self, session_id: str, db: Session):
        conversations = db.query(Interaction).filter(Interaction.session_id == session_id).all()
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


def get_character_websocket(data, character):
    data = json.loads(data["text"])
    model = "gpt-3.5-turbo"
    temperature = 0.1
    user_input = data["messageContent"]

    try:
        llm = get_llm(model, temperature, openai_api_key)
    except Exception as e:
        llm = None

    conversation_history = ConversationHistory()

    conversation_history.system_prompt = character.llm_system_prompt

    return llm, character, conversation_history, user_input