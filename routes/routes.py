from fastapi import APIRouter,Request, File, UploadFile, Depends, Form
import shutil
from typing import Optional
from pydantic import BaseModel
from os import getcwd, remove
import random
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from conf.db import con
from models.imagen import persona
from schemas.imagen import Imagen

routes = APIRouter()
#Base model
class Options (BaseModel):
    id:Optional[int] = Form()
    Nombre: str = Form()
    direccion: str = Form()
    dni: str = Form()
    
    
@routes.get("/")
async def get_all():
    return{
        "message": "Hola mundo"
    }
    

#Accept request as data and file
@routes.post("/uploadandacceptfile")
async def upload_accept_file(options: Options = Depends(),data: UploadFile = File(...)):
    data_options = options.dict()
    result = "Uploaded Filename: {}. JSON Payload{}".format(data.filename,data_options)
    return result


@routes.post("/basic")
async def post_basic_form(name :str = Form(...), apellido :str = Form(...), img: UploadFile = File(...)):
    with open(getcwd() +"/"+ img.filename, "wb") as myfile:
        content = await img.read()
        myfile.write(content)
        myfile.close()
    return {"name": name, "apellido": apellido, "imagen": img.filename}


''' @routes.post("/basic")
async def post_basic_form(file: UploadFile = File(...)):
    with open(getcwd() +"/"+ file.filename, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    return "success" '''

@routes.post("/basic-persona")
async def post_basic_form(name :str = Form(...), apellido :str = Form(...)):
    return {"name": name, "apellido": apellido}








''' ANDA!!! '''
@routes.post("/file_mysql", tags=["Personas"])
async def post_file(nombre :str = Form(...),apellido: str = Form(...),direccion: str = Form(...)
                    ,dni: str = Form(...),img: UploadFile = File(...)):
    with open(getcwd() +"/file/"+ img.filename, "wb") as myfile:
        route = getcwd() +"/file/"+ img.filename
        content = await img.read()
        myfile.write(content)
        myfile.close()
        print(route)
        id = random.randint(0,1000)
        new_image = {"id": id, "nombre": nombre, "apellido": apellido, "dni":dni, "direccion": direccion ,"dirImg": route}
        result = con.execute(persona.insert().values(new_image))
        return {
            "success": True,
            "message": "Se agrego la imagen",
        } 
        

@routes.get("/file_mysql/", tags=["Personas"])
async def get_files():
    result = con.execute(persona.select()).fetchall()
    return result

@routes.get("/file_mysql/{id}", tags=["Personas"])
async def get_on_file(id:int):
    result = con.execute(persona.select().where(persona.c.id == id)).first()
    img = FileResponse(result.dirImg)
    return {"id": result.id, "name": result.nombre, "apellido": result.apellido, "dni":result.dni, "direccion": result.direccion,
            "img": img}

@routes.delete("/file_mysql/{id}", tags=["Personas"])
async def delete_file(id:int):
    result = con.execute(persona.select().where(persona.c.id == id)).first()
    remove(result.dirImg)
    con.execute(persona.delete().where(persona.c.id == id)).first()
    return "Borrado"


@routes.put("/file_mysql/{id}", tags=["Personas"])
async def update_user(id:int, nombre :str = Form(...),apellido: str = Form(...),direccion: str = Form(...)
                    ,dni: str = Form(...),):

    con.execute(persona.update().values(nombre = nombre, apellido = apellido, dni = dni, direccion = direccion)
                .where(persona.c.id == id))
    return {
        "success": True,
        "message": "Se modifico los datos de la imagen"
    } 

@routes.put("/file_mysql_img/{id}", tags=["Personas"])
async def update_user(id:int, img: UploadFile = File(...)):

    result = con.execute(persona.select().where(persona.c.id == id)).first()
    remove(result.dirImg)

    with open(getcwd() +"/file/"+ img.filename, "wb") as myfile:
        route = getcwd() +"/file/"+ img.filename
        content = await img.read()
        myfile.write(content)
        myfile.close()
        print(route)
    con.execute(persona.update().values(dirImg = route).where(persona.c.id == id))
    return {
        "success": True,
        "message": "Se modifico los datos de la imagen"
    } 
    



















