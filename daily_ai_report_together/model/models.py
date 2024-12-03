import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anthropic
from utils.config import *
import openai
from openai import OpenAI
import anthropic
from utils.formats import *
import instructor


class LLM_Definition:
    @staticmethod
    def together_llm():
        global Together_API_KEY
        llm=openai.OpenAI(
                        base_url="https://api.together.xyz/v1",
                        api_key=Together_API_KEY,
                    )
        return llm

    @staticmethod
    def claude_llm():
        global Claude_API_KEY
        llm = anthropic.Anthropic(api_key=Claude_API_KEY)
        return llm

class Instructor_Definition:
    @staticmethod
    def together_inst(llm):
        client = instructor.from_openai(llm, mode=instructor.Mode.TOOLS)
        return client   

    @staticmethod
    def claude_inst(llm):
        client = instructor.from_anthropic(llm)
        return client