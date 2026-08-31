

from llms.llm_handler import LLMHandler


class RelevanceEvaluatorAgent:
    
    def __init__(self):
        
        
        self.llm_handler = LLMHandler(temperature=0.1)
        self.llm = self.llm_handler.get_llm().with_structured_output()