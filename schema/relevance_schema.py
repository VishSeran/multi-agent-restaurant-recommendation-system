from typing import Literal

from pydantic import BaseModel


class RelevanceSchema(BaseModel):
    
    query: str
    relevancy: Literal["CAN_ANSWER", "PARTIAL", "NO_MATCH"]