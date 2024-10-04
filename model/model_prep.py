from .prompt import *
import re
import httpx
import json
from utils.config import *
from .models import *
        
class Model:
    def __init__(self,llm):
        global system_prompt
        self.llm=llm
        self.call_res=[]
        self.mode={"openai.OpenAI":self.openai_cpl,
                 "anthropic.Anthropic":self.claude_cpl}

        model_type = str(type(self.llm))
        self.model_type = model_type[model_type.find("'")+1:model_type.rfind("'")]
        
    def __completion__(self,messages):
        model=self.mode[self.model_type]
        normal_completion=model(messages=messages)
        return normal_completion
    
    def __instructor__(self,messages,response_model):
        model=self.mode[self.model_type]
        structured_output=model(messages=messages,response_model=response_model)
        return structured_output

    def openai_cpl(self,messages,response_model=None):
        if response_model:
            llm_client=Instructor_Definition.openai_inst(self.llm)
            response = llm_client.chat.completions.create(
                model=openai_model_name,
                messages=messages,
                response_model=response_model
                )
            result = response.model_dump_json(indent=2)
            return result
        else:
            llm_client=self.llm
            response = llm_client.chat.completions.create(
                model=openai_model_name,
                messages=messages
                )

            response_message = response.choices[0].message
            return response_message.content

    def claude_cpl(self,messages,response_model=None):
        if response_model:
            llm_client=Instructor_Definition.claude_inst(self.llm)
            response = llm_client.messages.create(
                model=claude_model_name,
                max_tokens=2048,
                system=messages[0]["content"],
                messages=[messages[1]],
                response_model=response_model
            )
            result = response.model_dump_json(indent=2)
            return result
        else:
            llm_client=self.llm
            response = llm_client.messages.create(
                model=claude_model_name,
                max_tokens=2048,
                system=messages[0]["content"],
                messages=[messages[1]],
            )
            response_message=response.content
            return response_message[0].text