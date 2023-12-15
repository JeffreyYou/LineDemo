from fastapi import APIRouter, Depends, HTTPException, Path, WebSocket, WebSocketDisconnect, Query
from realtime_ai_character.character_catalog.catalog import CatalogManager, get_catalog_manager
from realtime_ai_character.utils import get_connection_manager, get_character_websocket
from realtime_ai_character.llm.openai_llm import get_llm, AsyncCallbackTextHandler
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
    
    session_auth = await check_session_auth(session_id, db, logger)

    await manager.connect(websocket)
    
    try:
        main_task = asyncio.create_task(
            handle_receive(session_id, websocket, db, session_auth))

        await asyncio.gather(main_task)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast_message(f"User #{session_id} left the chat")


async def handle_receive(session_id: str, websocket: WebSocket, db: Session, session_auth: SessionAuthResult):
    # callback function
    async def on_new_token(token) -> None:
        await manager.send_message(message=token,websocket=websocket)
    
    try:
        conversation_history = ConversationHistory()
        character = catalog_manager.get_character("LineDemo")
        conversation_history.system_prompt = character.llm_system_prompt
        if session_auth.is_existing_session:
            logger.info(f"User #{session_id} is loading from existing session")
            await asyncio.to_thread(conversation_history.load_from_db, session_id=session_id, db=db)

    
        while True:
            data = await websocket.receive()
            # data = json.dumps(data)
            print(data)
            if (data["type"] == "websocket.disconnect"):
                await manager.disconnect(websocket)
                return
            
            if (data["type"] == "websocket.receive"):

                
                llm, msg_data = get_character_websocket(data)

                # print(llm)
                # print(character)
                # print(ConversationHistory)

                if (llm == None):
                    await manager.send_message(
                            message="[Invalid_API_Setting]",
                            websocket=websocket) 
                    await manager.disconnect(websocket)
                    return
                response = await llm.achat(
                    history = build_history(conversation_history),
                    user_input = msg_data,
                    user_input_template = character.llm_user_prompt,
                    callback = AsyncCallbackTextHandler(on_new_token, [])
                )
                
                await manager.send_message(
                            message="[end_of_the_transmission]",
                            websocket=websocket)  
                
                # 4. Update conversation history
                conversation_history.user.append(msg_data)
                conversation_history.ai.append(response)   
                # 5. Persist interaction in the database
                interaction = Interaction(user_id=session_id,
                            session_id=session_id,
                            client_message_unicode=msg_data,
                            server_message_unicode=response,
                            platform="terminal",
                            action_type='text',
                            character_id=character.character_id)
                await asyncio.to_thread(interaction.save, db)   

    except WebSocketDisconnect:
        print(f"User #{phone_number} closed the connection")
        await manager.disconnect(websocket)
        return

