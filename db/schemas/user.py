def user_schema(user) -> dict: #-> para tipar lo que va a return
    return {"id": str(user["_id"]), #pasamos a str por si se gusrda de otro tipo en la bbdd
            "username": user["username"],
            "email": user["email"]}


def users_schema(users) -> list:
    return [user_schema(user) for user in users]

'''TRANSFORMAMOS LO QUE NOS VIENE DE BBDD A LA ESTRUCTURA DE NUESTRO MODELO (id por ejemplo es diferente)'''