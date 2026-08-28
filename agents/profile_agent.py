
import dotenv

from langchain_core.prompts import ChatPromptTemplate
from configurations.configs import GROQ_MODEL
from configurations.logger import get_logger
from llms.llm_handler import LLMHandler
from schema.user_profile import UserProfile


logger = get_logger("profile-agent")

dotenv.load_dotenv()

class ProfileAgent:
    
    def __init__(self):
        
        try:

            
            self.llm = LLMHandler(temperature=0.2)
            self.groq_chain = (self.llm.get_llm().with_structured_output(UserProfile))
            
            self.prompt = ChatPromptTemplate.from_messages( [
                (
                    "system",
                    """
                You are a restaurant user preference profiling agent.

                Analyze the user's historical restaurant reviews and infer
                stable dining preferences.

                Extract:
                
                - preferred cuisines
                - preferred foods
                - preferred flavor characteristics
                - preferred atmosphere
                - disliked atmosphere
                - dietary preferences
                - price sensitivity
                - any other useful restaurant preferences

                Do not infer preferences without evidence.

                Distinguish between:
                - something the user likes
                - something the user tolerated
                - something the user disliked
                """
                ),
                
                (
                    "human",
                    """
                    User ID:
                    {user_id}
                    
                    Review history:
                    {reviews} 
                    """
                    
                )
            ])
            
            self.chain = self.prompt | self.groq_chain
            logger.info("profile chain is created")
        
        except ValueError:
            logger.exception("Value error in profile agent init")
            raise
        
        except Exception:
            logger.exception("Error in profile agent init")
            raise 
        
        
    async def generate_profile(self, user_id:str, review_history:str) -> UserProfile:
        
        try:
            
            if not user_id:
                raise ValueError("User id is missing")
            
            if not review_history:
                raise ValueError("Review history is missing")
            
            response = await self.chain.ainvoke({
                "user_id": user_id,
                "reviews": review_history
            })
            
            logger.info("profile response is fetched")
            return response
            
        except ValueError:
            logger.exception("Value error in generate_profile")
            raise
        
        except Exception:
            logger.exception("Error in generate_profile")
            raise  