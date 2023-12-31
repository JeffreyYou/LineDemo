from fastapi import APIRouter, Depends, HTTPException, Path, WebSocket, WebSocketDisconnect, Query
from realtime_ai_character.character_catalog.catalog import CatalogManager, get_catalog_manager
from realtime_ai_character.utils import get_connection_manager, delete_chat_history, handle_request
from realtime_ai_character.llm.openai_llm import AsyncCallbackTextHandler
from realtime_ai_character.utils import ConversationHistory, build_history, SessionAuthResult, check_session_auth
from realtime_ai_character.database.connection import get_db
from realtime_ai_character.models.interaction import Interaction
from realtime_ai_character.logger import get_logger
from requests import Session

from dataclasses import dataclass
import asyncio
import json

router = APIRouter()
manager = get_connection_manager()
catalog_manager = get_catalog_manager()
logger = get_logger(__name__)



@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket,
                             session_id: str = Path(...),
                             api_key: str = Query(None),
                             llm_model: str = Query(None),
                             catalog_manager=Depends(get_catalog_manager),
                             db: Session = Depends(get_db)):
    

    await manager.connect(websocket)
    
    try:
        main_task = asyncio.create_task(
            handle_receive(session_id, websocket, db))

        await asyncio.gather(main_task)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast_message(f"User #{session_id} left the chat")


async def handle_receive(session_id: str, websocket: WebSocket, db: Session):
    # callback function
    async def on_new_token(token) -> None:
        await manager.send_message(message=token,websocket=websocket)
    
    try:


    
        while True:
            data = await websocket.receive()
            logger.info(f"Incoming request: {data}")

            
            if (data["type"] == "websocket.disconnect"):
                await manager.disconnect(websocket)
                return
            
            if (data["type"] == "websocket.receive"):
                # context initialization
                llm, message, character_name, operation = handle_request(data)
                character = catalog_manager.get_character(character_name)
                conversation_history = ConversationHistory()
                conversation_history.system_prompt = character.llm_system_prompt
                notification = character.notification
                
                # delete chat history if needed
                if operation == "delete_history":
                    delete_chat_history(character_name=character_name, session_id=session_id, db=db)
                    await manager.send_message(message=notification, websocket=websocket)
                    await manager.send_message(message="[end_of_the_transmission]", websocket=websocket)
                    conversation_history.ai = notification
                    interaction = Interaction(user_id=session_id,
                            session_id=session_id,
                            client_message_unicode="",
                            server_message_unicode=notification,
                            character_name = character_name)
                    await asyncio.to_thread(interaction.save, db)  
                    continue
                
                # load chat hisotry if there is any
                session_auth = await check_session_auth(session_id, character_name, db, logger)
                if session_auth.is_existing_session:
                    logger.info(f"User #{session_id} is loading from existing session")
                    await asyncio.to_thread(conversation_history.load_from_db, session_id=session_id, character_name=character_name , db=db)


                if (llm == None):
                    await manager.send_message(message="[Invalid_API_Setting]", websocket=websocket) 
                    await manager.disconnect(websocket)
                    return
                
                response = await llm.achat(
                    history = build_history(conversation_history),
                    user_input = message,
                    user_input_template = character.llm_user_prompt,
                    callback = AsyncCallbackTextHandler(on_new_token, [])
                )
                
                await manager.send_message(message="[end_of_the_transmission]", websocket=websocket)  
                
                # 4. Update conversation history
                conversation_history.user.append(message)
                conversation_history.ai.append(response)   
                # 5. Persist interaction in the database
                interaction = Interaction(user_id=session_id,
                            session_id=session_id,
                            client_message_unicode=message,
                            server_message_unicode=response,
                            character_name = character_name)
                await asyncio.to_thread(interaction.save, db)   

    except WebSocketDisconnect:
        print(f"User #{session_id} closed the connection")
        await manager.disconnect(websocket)
        return

