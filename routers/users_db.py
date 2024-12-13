### Users API ###

from fastapi import APIRouter, HTTPException, status
from db.model.user import User
from db.client import db_cliente
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

# Inicia el server: uvicorn users:app --reload

app_users = APIRouter(prefix="/userdb", 
                         tags=["userdb"],#para en la documentacion /docs ver los productos organizados
                         responses= {status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@app_users.get("/", response_model=list[User])
async def users():
    return users_schema(db_cliente.users.find())  #devuelve todos


@app_users.get("/{id}")  # Path
async def user(id: str):
    return search_user("_id",ObjectId(id))


@app_users.get("/")  # Query
async def user(id: str):
    return search_user("_id",ObjectId(id))



@app_users.post("/", response_model=User, status_code=status.HTTP_201_CREATED )#insertar datos (json escrito)
async def user(user: User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    user_diccio = dict(user) #lo pasamos a diccionario ya que mongo trabaja con json que vienen a ser diccionarios
    del user_diccio["id"] #lo borramos por si acaso

    id = db_cliente.users.insert_one(user_diccio).inserted_id

    new_user = user_schema(db_cliente.users.find_one({"_id":id})) #mongo llama al id  _id

    

    return User(**new_user)


@app_users.put("/", response_model=User)#actualizar datos usar mismo json cambiando algun campo
async def user(user: User):
 
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_cliente.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))

@app_users.delete("/{id}")
async def user(id: str):

    found = db_cliente.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}


def search_user_by_email(email: str):

    try:
        user = db_cliente.users.find_one({"email": email})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
    

def search_user(field: str, key):

    try:
        user = db_cliente.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
 