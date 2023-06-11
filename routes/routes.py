import json
from pprint import pprint
from fastapi import APIRouter,Request, File, UploadFile, Depends, Form, HTTPException, status
import shutil
from typing import Optional
from pydantic import BaseModel
from os import getcwd, remove
import random
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse


from conf.db import con
from models.persona import persona

routes = APIRouter()


@routes.get("/")
async def get_all():
    return{
        "message": "Hola mundo"
    }
    

@routes.post("/persona_file/", tags=["Personas"])
async def post_file(nombre :str = Form(...),apellido: str = Form(...),direccion: str = Form(...)
                    ,dni: str = Form(...),img: UploadFile = File(...)):
    with open(getcwd() +"/file/"+ img.filename, "wb") as myfile:
        route = getcwd() +"/file/"+ img.filename
        content = await img.read()
        myfile.write(content)
        myfile.close()
        print(route)
        id = random.randint(0,100)
        new_image = {"id": id, "nombre": nombre, "apellido": apellido, "dni":dni, "direccion": direccion ,"dirImg": route}
        con.execute(persona.insert().values(new_image))
        con.commit()
        return {
            "success": True,
            "message": "La persona se agrego correcctamente",
        } 
        

@routes.get("/persona_file/", tags=["Personas"])
async def get_files():
    result = con.execute(persona.select()).fetchall()
    pprint(result)
    try:
        response = []
        for data in result:
            img = FileResponse(data.dirImg)
            response.append({
                    "nombre": data.nombre,
                    "apellido": data.apellido,
                    "dni": data.dni,
                    "direccion": data.direccion,
                    "dirImg": img
                    })
        return response
    except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error en solicitud") from err

@routes.get("/persona_file/{id}", tags=["Personas"])
async def get_on_file(id:int):
    result = con.execute(persona.select().where(persona.c.id == id)).first()
    pprint(result)
    if result == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la persona ingresada"
        )
    try:
        img = FileResponse(result.dirImg)
        return {
            "id": result.id,
            "name": result.nombre,
            "apellido": result.apellido,
            "dni":result.dni,
            "direccion": result.direccion,
            "img": img
            }
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error en solicitud") from err

@routes.delete("/persona_file/{id}", tags=["Personas"])
async def delete_file(id:int):
    result = con.execute(persona.select().where(persona.c.id == id)).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la persona ingresada"
        )
    remove(result.dirImg)
    con.execute(persona.delete().where(persona.c.id == id)).first()
    con.commit()
    return "Borrado"


@routes.put("/persona_file/{id}", tags=["Personas"])
async def update_user(id:int, nombre :str = Form(...),apellido: str = Form(...),direccion: str = Form(...)
                    ,dni: str = Form(...),):
    result = con.execute(persona.select().where(persona.c.id == id)).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la persona ingresada"
        )
    con.execute(persona.update().values(nombre = nombre, apellido = apellido, dni = dni, direccion = direccion)
                .where(persona.c.id == id))
    con.commit()
    return {
        "success": True,
        "message": "Se modifico los datos de la imagen"
    } 

@routes.put("/persona_file_img/{id}", tags=["Personas"])
async def update_user(id:int, img: UploadFile = File(...)):

    result = con.execute(persona.select().where(persona.c.id == id)).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la persona ingresada"
        )
    remove(result.dirImg)

    with open(getcwd() +"/file/"+ img.filename, "wb") as myfile:
        route = getcwd() +"/file/"+ img.filename
        content = await img.read()
        myfile.write(content)
        myfile.close()
        print(route)
    con.execute(persona.update().values(dirImg = route).where(persona.c.id == id))
    con.commit()
    return {
        "success": True,
        "message": "Se modifico los datos de la imagen"
    }
