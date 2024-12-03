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
    def openai_llm():
        global Openai_API_KEY
        llm = OpenAI(api_key=Openai_API_KEY)
        return llm

    @staticmethod
    def claude_llm():
        global Claude_API_KEY
        llm = anthropic.Anthropic(api_key=Claude_API_KEY)
        return llm

class Instructor_Definition:
    @staticmethod
    def openai_inst(llm):
        client = instructor.from_openai(llm)
        return client

    @staticmethod
    def claude_inst(llm):
        client = instructor.from_anthropic(llm)
        return client