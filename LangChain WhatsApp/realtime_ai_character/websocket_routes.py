from fastapi import APIRouter, Depends, HTTPException, Path, WebSocket, WebSocketDisconnect, Query
from realtime_ai_character.character_catalog.catalog import CatalogManager, get_catalog_manager
from realtime_ai_character.utils import get_connection_manager, delete_chat_history, handle_request, handle_request_image,chaining_picture_rag
from realtime_ai_character.llm.openai_llm import AsyncCallbackTextHandler
from realtime_ai_character.utils import ConversationHistory, build_history, build_history_image, check_session_auth, chaining_user_info, delete_user_history, chaining_question_rag
from realtime_ai_character.database.connection import get_db
from realtime_ai_character.models.interaction import Interaction
from realtime_ai_character.models.user import User
from realtime_ai_character.logger import get_logger
from requests import Session
from dotenv import load_dotenv

from dataclasses import dataclass
import asyncio
import os


router = APIRouter()
manager = get_connection_manager()
catalog_manager = get_catalog_manager()
logger = get_logger(__name__)



load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

image_map = {}



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
    async def on_new_token_null(token) -> None:
        pass
    
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
                if operation == "image_read":
                    res = handle_request_image(data, session_id, image_map)
                    # picture_description = json.loads(res)["descriptionIfNot"]
                    #send response message to user
                    character = catalog_manager.get_character(character_name)
                    conversation_history = ConversationHistory()
                    session_auth = await check_session_auth(session_id, character_name, db, logger)
                    # if session_auth.is_existing_session:
                    #     logger.info(f"User #{session_id} is loading chat history from existing session")
                    #     await asyncio.to_thread(conversation_history.load_from_db, session_id=session_id, character_name=character_name , db=db)
                    conversation_history.system_prompt =  f"""圖片內容\n###\n用戶跟你分享了一張圖片,圖片的內容已經被一個"json文件"所概括，其中isInvestment的yes表示這張圖是否是交易截圖, 如果是交易截圖則pictureInfo包含了交易的信息，isInvestment的no表示不是交易截圖，其中descriptionIfNot包含了這張非交易截圖的描述\n###\njson文件###\n{res}###\n你的職責\n###如果是交易截圖，你就表示恭喜你買了多少股，只有购买，没有卖出，只說股票代碼，不說股票名稱，如果成交數量有內容，沒讀取則不發數量，如果不是交易截圖,請你根據這descriptionIfNot的內容感謝用戶的分享，並非常簡短的表達一下你看到這張圖片開心的心情,用中文回答，不要讓人看出來你是ai\n###"""
                    print(conversation_history)
                    response = await llm.achat(
                        history = build_history_image(conversation_history, conversation_history.system_prompt),
                        user_input = "",
                        user_input_template = character.llm_user_prompt,
                        callback = AsyncCallbackTextHandler(on_new_token, [])
                    )
                    await manager.send_message(message="[end_of_the_transmission]", websocket=websocket) 
                    continue
                    
                character = catalog_manager.get_character(character_name)
                conversation_history = ConversationHistory()
                conversation_history.system_prompt = character.llm_system_prompt
                notification = character.notification
                
                if operation == "delete_history":
                    delete_chat_history(character_name=character_name, session_id=session_id, db=db)
                    if (character.name == "DemoDay01"):
                        delete_user_history(user_id=session_id, db=db)
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
                
                session_auth = await check_session_auth(session_id, character_name, db, logger)
                if session_auth.is_existing_session:
                    logger.info(f"User #{session_id} is loading chat history from existing session")
                    await asyncio.to_thread(conversation_history.load_from_db, session_id=session_id, character_name=character_name , db=db)

                if (llm == None):
                    await manager.send_message(message="[Invalid_API_Setting]", websocket=websocket) 
                    await manager.disconnect(websocket)
                    return
                
                if (character.name != "DemoDay01"):
                    await chaining_user_info(session_id=session_id, db=db, logger=logger, conversation_history=conversation_history, catalog_manager=catalog_manager, llm=llm, on_new_token_null=on_new_token_null)
                        
                chaining_question_rag(catalog_manager, conversation_history, message, logger)
                chaining_picture_rag(conversation_history, session_id, image_map)
                print(conversation_history.system_prompt)
                
                response = await llm.achat(
                    history = build_history(conversation_history),
                    user_input = message,
                    user_input_template = character.llm_user_prompt,
                    callback = AsyncCallbackTextHandler(on_new_token, [])
                )
                
                await manager.send_message(message="[end_of_the_transmission]", websocket=websocket) 

                
                conversation_history.user.append(message)
                conversation_history.ai.append(response)   
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

