from pymongo import MongoClient

#pip install pymongo

#para local
#db_cliente = MongoClient().local




db_cliente = MongoClient("mongodb+srv://hawkent:$Mongo05$@cluster0.7trqi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", serverSelectionTimeoutMS=50000, ssl=True, ssl_certfile=None, ssl_ca_certs=None).nube

