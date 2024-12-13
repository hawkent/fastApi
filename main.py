from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_oauth_users, users_db #traemos productos de la carpeta router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
#iniciar server  uvicorn main:app --reload 
@app.get("/")# / es localhost http://127.0.0.1:8000
async def root():#siempre que llamamos a servidor tiene que ser asincrona para que no se quede esperando hasta que cargue y pueda hacer otras cosasuvicorn main:app --reload 
    return "Hola fastAPI"

@app.get("/url")# / es localhost http://127.0.0.1:8000/url
async def root():#siempre que llamamos a servidor tiene que ser asincrona para que no se quede esperando hasta que cargue y pueda hacer otras cosasuvicorn main:app --reload 
    return { "Url_coches":"https://coches.net" }



'''http://127.0.0.1:8000/docs    ESTO GENERA LA DOCUMENTACION AUTOMATICAMENTE SWAGGER'''
'''http://127.0.0.1:8000/redoc    IGUAL PERO USANDO OTRO ESTANDAR DE DOCUMENTACION REDOCLY'''

'''ctrl c para detener el server'''



#Router
app.include_router(products.app_products)
app.include_router(users.app_users)
app.mount("/static", StaticFiles(directory="static"), name="static") # http://127.0.0.1:8000/static/images/python.png
app.include_router(basic_auth_users.router)
app.include_router(jwt_oauth_users.router)
app.include_router(users_db.app_users)