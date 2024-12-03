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
        self.mode={"openai.OpenAI":self.together_cpl,
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

    def together_cpl(self,messages,response_model=None):
        if response_model:
            max_retries=25
            for attempt in range(max_retries):
                print('instruct cpl try',attempt)
                try:
                    llm_client = Instructor_Definition.together_inst(self.llm)
                    # print("++ 1 ++")
                    response = llm_client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                        response_model=response_model,
                        messages=messages,
                    )
                    # print("++ 2 ++")
                    return [{"title": rc.title, "category": rc.category} for rc in response.categories]
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    continue
        else:
            llm_client=self.llm
            response = llm_client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                messages=messages,
                # temperature=0,
                # top_p=0.7,
                # top_k=50,
                # repetition_penalty=1,
                # stop=["<|eot_id|>","<|eom_id|>"],
                )
  
            response_message = response.choices[0].message
            return response_message.content
