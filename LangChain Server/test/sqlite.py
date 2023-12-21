import uuid
from realtime_ai_character.models.interaction import Interaction
from realtime_ai_character.database.connection import get_db
from realtime_ai_character.utils import ConversationHistory, build_history
from requests import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith(
    "sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

conversation_history = ConversationHistory()
user = ["你好", "我叫Jeffrey"]
ai = ["你好,我叫Isabel,很高兴认识你,你希望我怎么称呼你", "你好Jeffrey,今天很忙吗"]
conversation_history.user.extend(user)
conversation_history.ai.extend(ai)

session_id = str(uuid.uuid4().hex)
message_id = str(uuid.uuid4().hex)[:16]
tools = []
interaction = Interaction(  user_id=session_id,
                            session_id=session_id,
                            client_message_unicode="can you do me a favor?",
                            server_message_unicode="yes, of course.",
                            platform="terminal",
                            action_type='text',
                            character_id="Line Demo",
                            language="English",
                            message_id=message_id,
                            )

db = SessionLocal()
db.add(interaction)
# conversations = db.query(Interaction).all()
db.commit()
# for conversation in conversations:
#     print(f"ID: {conversation.user_id}, Message: {conversation.client_message_unicode}")

db.close()
