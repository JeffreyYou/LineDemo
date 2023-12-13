from fastapi import APIRouter, Depends, HTTPException, Path, WebSocket, WebSocketDisconnect, Query
from catalog import CatalogManager, get_catalog_manager
from utils import get_connection_manager, get_character_websocket
import asyncio
import json
from openai_llm import get_llm, AsyncCallbackTextHandler
from utils import ConversationHistory, build_history

router = APIRouter()
manager = get_connection_manager()

@router.websocket("/ws/{phone_number}")
async def websocket_endpoint(websocket: WebSocket,
                             phone_number: str = Path(...),
                             api_key: str = Query(None),
                             llm_model: str = Query(None),
                             catalog_manager=Depends(get_catalog_manager)):

    await manager.connect(websocket)
    
    try:
        main_task = asyncio.create_task(
            handle_receive(websocket, phone_number, catalog_manager))

        await asyncio.gather(main_task)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast_message(f"User #{phone_number} left the chat")


async def handle_receive(websocket: WebSocket, phone_number: str, catalog_manager: CatalogManager):
    async def on_new_token(token) -> None:
        await manager.send_message(message=token,
                            websocket=websocket)
    
    try:
        while True:
            data = await websocket.receive()
            # data = json.dumps(data)
            print(data)
            if (data["type"] == "websocket.disconnect"):
                await manager.disconnect(websocket)
                return
            
            if (data["type"] == "websocket.receive"):

                catalog_manager = get_catalog_manager()
                character = catalog_manager.get_character("LineDemo")
                
                llm, character, conversation_history, user_input = get_character_websocket(data, character)
                print(llm)

                # print(character)
                # print(ConversationHistory)

                if (llm == None):
                    await manager.send_message(
                            message="[Invalid_API_Setting]",
                            websocket=websocket) 
                    await manager.disconnect(websocket)
                    return
                await llm.achat(
                    history = build_history(conversation_history),
                    user_input = user_input,
                    user_input_template = character.llm_user_prompt,
                    callback = AsyncCallbackTextHandler(on_new_token, [])
                )
                
                await manager.send_message(
                            message="[end_of_the_transmission]",
                            websocket=websocket)          

    except WebSocketDisconnect:
        print(f"User #{phone_number} closed the connection")
        await manager.disconnect(websocket)
        return

