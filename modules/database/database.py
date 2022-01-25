from pymongo import MongoClient
from bson.objectid import ObjectId
import secrets
import os

"""
Os métodos abaixo compõem um módulo que realiza operações básicas do banco
de dados MongoDB.
"""
def connect():
    # instânciando o cliente do mongo
    client = MongoClient(os.environ['MONGO_URI'])
    
    # se não existe conexão com o banco return antes
    if client is None:
        return
    
    # criando o banco
    database = client['chatbot']

    # criando uma colections
    requests_collection = database['requests']
    return requests_collection

# gera um token aleatorio
def ramdom_token():
    return secrets.token_urlsafe(40)

# insere os dados no banco
# retorna o id do objeto e o token de acesso para o usuário
def insert(**kwargs):
    if kwargs:
        requests_collection = connect()
        token = ramdom_token()
        
        try:
            kwargs.update({'post_status': 'não postado'})
            kwargs.update({'token': token})
            id = requests_collection.insert_one(kwargs)
            id_document = id.inserted_id
            print(id_document)
            return id_document, token
        except Exception as e:
            print(e)
            return -1, ''

    else:
        print('Nenhum dado foi informado')
    return -1, ''

# busca um documento no banco pelo seu id
def get_by_id(objectid):
    requests_collection = connect()
    try:
        res = requests_collection.find_one({'_id': ObjectId(objectid)})
        return res
    except Exception as e:
        print(e)
        return None