from pymongo import MongoClient, DESCENDING
from datetime import timezone
import secrets

"""
Os métodos abaixo compõem um módulo que realiza operações básicas do banco
de dados MongoDB.
"""

def connect():
    # instânciando o cliente do mongo
    client = MongoClient('mongodb://root:root@localhost:27017/')

    # criando o banco
    database = client['chatbot']

    # criando uma colections
    requests_collection = database['requests']
    return requests_collection

def ramdom_token():
    return secrets.token_urlsafe(40)

def insert(**kwargs):
    if kwargs:
        requests_collection = connect()
        token = ramdom_token()
        kwargs.update({'post_status': 'não postado'})
        kwargs.update({'token': token})
        id = requests_collection.insert_one(kwargs)
        id_document = id.inserted_id
        print(id_document)
        return id_document, token
    else:
        print('nenhum dado foi informado')

    return -1

def get_all_data():
    requests_collection = connect()
    all_documents = []
    
    """
    Realização de uma query que obtem todos os documentos existentes no
    banco de dados, os ordena de modo decresente pela sua data de inserção
    e remove o campo "__id" adicionado automaticamente pelo MongoDB.
    """
    for document in requests_collection.find({}, {'_id': False}).sort('date', DESCENDING):
        # se existir documento
        if (document):
            # converte UTC para horario local
            local_date = document['date'].replace(tzinfo=timezone.utc).astimezone(tz=None)
            #  converte para o formato dd/mm/yy hh:mm
            document['date'] = local_date.strftime("%d/%m/%Y %H:%M")
            all_documents.append(document)
    
    return all_documents

from bson.objectid import ObjectId
def get_by_id(objectid):
    # objInstance = ObjectId('61ebebf2fdcc0b70da85144e')
    requests_collection = connect()
    res = requests_collection.find_one({'_id': ObjectId('61ebe1794b3fd1d6371c8d1c')})
    return res