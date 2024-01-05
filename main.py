from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pymongo

#libreria para el manejo de versiones
from versioned_fastapi import version, FastApiVersioner

app = FastAPI(
    title="Api Persona - Segundo bimestre",
    description="API para el manejo de presonas segundo parcial",
    version="1.0.1",
    contact={
        "name": "Ricardo Yunhon",
        "email": "asistemacomp@gmail.com",
        "url":"www.google.com",
    },
    license_info={
        "name":"Desarrolladores",
        "url":"www.google.com",
    },
    openapi_tags={
        "name": "Persona",
        "description":"operacion del Manejo de personas",
    }

)

# Modelo de datos para un pedido
class Pedido(BaseModel):
    detalle: str
    cantidad: int
    mesa: int
    mesero: str    

# Lista para almacenar pedidos (simulación de base de datos)
pedido_db = []

# Operación para crear un pedido
@version(1)
@app.post("/pedido/", response_model=Pedido )
def create_pedido(pedido: Pedido):
    pedido_db.append(pedido)
    return pedido

# Operación para obtener todas los pedidos
@version(1)
@app.get("/pedido/", response_model=List[Pedido])
def get_all_pedido():
    return pedido_db

# Operación para obtener un pedido por ID
@version(1)
@app.get("/pedido/{pedido_id}", response_model=Pedido)
def get_pedido_by_id(pedido_id: int):
    for pedido in pedido_db:
        if pedido.id == pedido_id:
            return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Operación para editar un pedido por ID
@version(1)
@app.put("/pedido/{pedido_id}", response_model=Pedido)
def update_pedido(pedido_id: int, updated_pedido: Pedido):
    for index, person in enumerate(pedido_db):
        if person.id == pedido_id:
            pedido_db[index] = updated_pedido
            return updated_pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Operación para eliminar un pedido por ID
@version(1)
@app.delete("/pedido/{pedido_id}", response_model=Pedido)
def delete_pedido(pedido_id: int):
    for index, pedido in enumerate(pedido_db):
        if pedido.id == pedido_id:
            deleted_pedido = pedido_db.pop(index)
            return deleted_pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Version your app
# It will add version prefixes and customize the swagger docs
versions = FastApiVersioner(app).version_fastapi()