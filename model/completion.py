import json
import openai
from typing import List, Dict, Union
from .model_prep import Model
from utils.config import *
from utils.formats import *

class Completion(Model):
    def __init__(self, llm):
        super().__init__(Completion)
        self.llm = llm
        self.model=Model(self.llm)
        self.messages = []

    def __call__(self, message, system_prompt):
        self.messages.append({"role": "system", "content":system_prompt})
        self.messages.append({"role": "user", "content": message})
        
        response = self.execute()
        return response
        
    def execute(self):
        response=self.model.__completion__(self.messages)
        return response

class Instructor(Model):
    def __init__(self, llm):
        super().__init__(Completion)
        self.llm = llm
        self.response_model=Output_format
        self.model=Model(self.llm)
        self.messages = []

    def __call__(self, message, system_prompt):
        self.messages.append({"role": "system", "content": system_prompt})
        self.messages.append({"role": "user", "content": message})
        
        response = self.execute()
        return response
        
    def execute(self):
        response=self.model.__instructor__(self.messages, self.response_model)
        return response