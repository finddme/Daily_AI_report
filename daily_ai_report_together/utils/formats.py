from typing_extensions import TypedDict
from typing import List
from pydantic import BaseModel, Field,model_serializer
from pydantic import TypeAdapter
from typing import List

class Category(BaseModel):
    title:str
    category:str

class Output_format(BaseModel):
    categories: List[Category]
