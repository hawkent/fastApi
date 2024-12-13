from pydantic import BaseModel
from typing import Optional

class User(BaseModel):#basemodel 
    id: Optional[str] = None  #para decirle que es opcional asi no lo rellenamos nosotros pero a la hora de recogerlo de la bbdd si existe porque mongo lo crea automatico
    username: str
    email: str
