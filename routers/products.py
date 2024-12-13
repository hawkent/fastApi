'''USAMOS ROUTERS PORQUE ASI PODEMOS LLAMAR A TODOS DESDE EL MISMO SERVER'''
#from fastapi import FastAPI (ESTO SI SOLO ES UNA API Y NO HAY ROUTERS)
from fastapi import APIRouter

app_products = APIRouter(prefix="/products", 
                         tags=["products"],#para en la documentacion /docs ver los productos organizados
                         responses= {404: {"message": "No encontrado"}})
# Inicia el server: uvicorn products:app --reload


products_list = ["Producto 1","Producto 2","Producto 3","Producto 4","Producto 5"]

@app_products.get("/")#"/products" sin el prefix
async def products():
    return products_list


@app_products.get("/{id}")#"/products/{id}" sin el prefix
async def products(id : int):
    return products_list[id]