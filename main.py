from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pymongo
from bson.objectid import ObjectId

#libreria para generar un id unico
import uuid

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://rsyunhonop:m0n1c4120.Ec@cluster0.xpefy.mongodb.net/?retryWrites=true&w=majority")
database = cliente["Interoperatividad"]
coleccion = database["apiPedido"]

#libreria para el manejo de versiones
#from versioned_fastapi import version, FastApiVersioner

app = FastAPI(
    title="API de pedidos del segundo parcial",
    description="API para el manejo de pedidos en el segundo parcial de la materia de Interoperabilidad",
    version="1.0.1",
    contact={
        "name": "Ricaro Yunhon",
        "email": "rsyunhon@utpl.edu.ec",
        "url": "https://github.com/rsyunhon/Utpl.Interoperabilidad.Api.2023"
    },
    license_info={
        "name": "MIT License",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    openapi_tags=[
        {
            "name": "Pedido",
            "description": "Operaciones para el manejo de pedidos"
        }
    ]
)

# Modelo de datos para un pedido
class Pedido(BaseModel):
    detalle: str
    cantidad: int
    mesa: int
    mesero: str
    pedidoNumero: int    

# Modelo de repositorio para un pedido
class PedidoRepositorio(BaseModel):
    id: str
    detalle: str
    cantidad: int
    mesa: int
    mesero: str 
    pedidoNumero: int
    id: str 


# Lista para almacenar pedidos (simulación de base de datos)
# pedido_db = []

# Operación para crear un pedido
#@version(1)
@app.post("/pedido/", response_model=PedidoRepositorio, tags=["Pedido"] )
def create_pedido(pedido: Pedido):
    idPedido=str(uuid.uuid4())
    itemPedido = PedidoRepositorio(id=idPedido, **pedido.dict()) 
    #detalle=pedido.detalle, cantidad=pedido.cantidad, mesa=pedido.mesa, mesero=pedido.mesero, pedidoNumero=pedido.pedidoNumero,  id=idPedido)
    result = coleccion.insert_one(itemPedido.dict())
    return itemPedido

# Operación para obtener todas los pedidos
#@version(1)
@app.get("/pedido/", response_model=List[PedidoRepositorio], tags=["Pedido"])
def get_all_pedido():
    items = list(coleccion.find())
    pedidos = [PedidoRepositorio(id=str(item["_id"]), **item) for item in items]
    return pedidos

# Operación para obtener un pedido por ID
#@version(1)
@app.get("/pedido/{pedido_id}", response_model=PedidoRepositorio, tags=["Pedido"])
def get_pedido_by_id(pedido_id: str):
    item = coleccion.find_one({"_id": ObjectId(pedido_id)})
    if item:
        return PedidoRepositorio(id=str(item["_id"]), **item)
    else:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Operación para editar un pedido por ID
#@version(1)
@app.put("/pedido/{pedido_id}", response_model=PedidoRepositorio, tags=["Pedido"])
def update_pedido(pedido_id: str, updated_pedido: Pedido):
    result = coleccion.update_one(
        {"_id": ObjectId(pedido_id)},
        {"$set": updated_pedido.dict()}
    )
    if result.matched_count:
        return PedidoRepositorio(id=pedido_id, **updated_pedido.dict())
    else:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Operación para eliminar un pedido por ID
#@version(1)
@app.delete("/pedido/{pedido_id}", response_model=PedidoRepositorio, tags=["Pedido"])
def delete_pedido(pedido_id: str):
    item = coleccion.find_one_and_delete({"_id": ObjectId(pedido_id)})
    if item:
        return PedidoRepositorio(id=str(item["_id"]), **item)
    else:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Operación para obtener una pedido por identificacion
#@version(1)
@app.get("/pedido/mesa/{mesa}", response_model=Pedido, tags=["Pedido"])
def get_pedido_by_mesa(mesa: int):
    item = coleccion.find_one({"mesa": mesa})
    if item:
        return PedidoRepositorio(id=str(item["_id"]), **item)
    else:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")


# Version your app
# It will add version prefixes and customize the swagger docs
#versions = FastApiVersioner(app).version_fastapi()
