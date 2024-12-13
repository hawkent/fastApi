'''mas seguro al estar encriptando la contraseña'''

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime ,timedelta

ALGORIMO = "HS256"
DURACION_TOKEN = 1
SECRET = "as89fghjsfhj124uyjxyrr741qpzr33hfd3qg2aahjf"


#iniciar server  uvicorn jwt_oauth_users:app --reload 
#pip install "python-jose[cryptography]"
#pip install "passlib[bcrypt]"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])  

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "$2a$12$QUstllbsRaYY/Qmuin6hn.RWLlWvTnrOcCixUZQZF8zw1OeTuDYQm"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)


    if not crypt.verify(form.password, user.password): #verifica si concuerda lo que metemos con lo guardado                             
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")


    expira = datetime.utcnow() + timedelta(minutes=DURACION_TOKEN)

    token = {"sub":user.username, "exp": expira}

    return {"access_token": jwt.encode(token, SECRET, algorithm=ALGORIMO), "token_type": "bearer"}


'''Con un decoder de hs256 vemos lo que sacar el post'''


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORIMO]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user 


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user