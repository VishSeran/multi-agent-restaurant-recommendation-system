import os

import dotenv
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from configurations.configs import GROQ_MODEL
from configurations.logger import get_logger

logger = get_logger("llm-handler")

dotenv.load_dotenv()


class LLMHandler:

    def __init__(self):

        try:

            self.model_name = GROQ_MODEL

            api_key = os.getenv("GROQ_API")

            if not api_key:
                raise ValueError(
                    "Groq API key is missing"
                )

            self.chat_groq = ChatGroq(
                model=self.model_name,
                api_key=api_key,
                max_tokens=5000,
                verbose=True
            )

            self.checkpointer = InMemorySaver()

            logger.info(
                "ChatGroq and checkpointer created"
            )

        except Exception:
            logger.exception(
                "Error in LLM handler"
            )
            raise
        
    
    def get_llm(self) -> ChatGroq:
        
        return self.chat_groq
    
    async def get_llm_response(self, query):
        
        try:
            
            if not query:
                raise ValueError("Query is missing")
            
            response = await self.chat_groq.ainvoke(query)
            logger.info("response is fetched")
            return response.content
            
        except ValueError:
            logger.exception("Value error in get_llm_response")
            raise
        
        except Exception:
            logger.exception("Error in get_llm_response")
            raise