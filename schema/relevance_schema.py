from pydantic import BaseModel


class RelevanceSchema:
    
    query: str
    relevancy: str