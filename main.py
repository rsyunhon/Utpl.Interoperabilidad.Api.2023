from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos para un pedido
class Pedido(BaseModel):
    detalle: str
    cantidad: int
    mesa: int
    mesero: str
    id: int

# Lista para almacenar pedidos (simulación de base de datos)
pedido_db = []

# Operación para crear un pedido
@app.post("/pedido/", response_model=Pedido)
def create_pedido(pedido: Pedido):
    pedido_db.append(pedido)
    return pedido

# Operación para obtener todas los pedidos
@app.get("/pedido/", response_model=List[Pedido])
def get_all_pedido():
    return pedido_db

# Operación para obtener un pedido por ID
@app.get("/pedido/{pedido_id}", response_model=Pedido)
def get_pedido_by_id(pedido_id: int):
    for pedido in pedido_db:
        if pedido.id == pedido_id:
            return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Operación para editar un pedido por ID
@app.put("/pedido/{pedido_id}", response_model=Pedido)
def update_pedido(pedido_id: int, updated_pedido: Pedido):
    for index, person in enumerate(pedido_db):
        if person.id == pedido_id:
            pedido_db[index] = updated_pedido
            return updated_pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Operación para eliminar un pedido por ID
@app.delete("/pedido/{pedido_id}", response_model=Pedido)
def delete_pedido(pedido_id: int):
    for index, pedido in enumerate(pedido_db):
        if pedido.id == pedido_id:
            deleted_pedido = pedido_db.pop(index)
            return deleted_pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")
