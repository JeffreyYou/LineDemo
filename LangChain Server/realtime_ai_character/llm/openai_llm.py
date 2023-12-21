from abc import ABC, abstractmethod
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import AsyncCallbackHandler
from typing import List


class LLM(ABC):
    @abstractmethod
    async def achat(self, *args, **kwargs):
        pass

class AsyncCallbackTextHandler(AsyncCallbackHandler):
    def __init__(self, on_new_token=None, token_buffer=None, on_llm_end=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_new_token = on_new_token
        self._on_llm_end = on_llm_end
        self.token_buffer = token_buffer

    async def on_chat_model_start(self, *args, **kwargs):
        pass

    async def on_llm_new_token(self, token: str, *args, **kwargs):
        if self.token_buffer is not None:
            self.token_buffer.append(token)

        await self.on_new_token(token)

    async def on_llm_end(self, *args, **kwargs):
        if self._on_llm_end is not None:
            await self._on_llm_end(''.join(self.token_buffer))
            self.token_buffer.clear()


class OpenaiLlm(LLM):
    def __init__(self, model, temperature, api_key):

        self.chat_open_ai = ChatOpenAI(
            model=model,
            temperature=temperature,
            streaming=True,
            openai_api_key=api_key
        )
        self.config = {
            "model": model,
            "temperature": temperature,
            "streaming": True
        }

    async def achat(self,
                    history: List[BaseMessage],
                    user_input: str,
                    user_input_template: str,
                    callback: AsyncCallbackTextHandler,
                    metadata: dict = None,
                    *args, **kwargs) -> str:

        history.append(HumanMessage(content=user_input_template.format(
            context='\n', query=user_input)))
        
        response = await self.chat_open_ai.agenerate(
            [history], callbacks=[callback, StreamingStdOutCallbackHandler()],
            metadata=metadata)
        # response = await self.chat_open_ai.agenerate(
        #     [history], callbacks=[StreamingStdOutCallbackHandler()],
        #     metadata=metadata)
        # response = await self.chat_open_ai.agenerate(
        #     [history], callbacks=[callback],
        #     metadata=metadata)
        return response.generations[0][0].text

def get_llm(model, temperature, api_key) -> LLM:
    if model.startswith('gpt'):
        from realtime_ai_character.llm.openai_llm import OpenaiLlm
        return OpenaiLlm(model=model, temperature=temperature, api_key=api_key)