from typing import Optional
from pydantic import BaseModel
from fastapi import Form


class Persona (BaseModel):
    id:Optional[str] 
    nombre:str
    apellido:str
    direccion:str 
    dni:str
    dirImg:str
    