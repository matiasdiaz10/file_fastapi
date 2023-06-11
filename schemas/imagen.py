from typing import Optional
from pydantic import BaseModel
from fastapi import Form


class Imagen(BaseModel):
    id:Optional[str] 
    name:str 
    