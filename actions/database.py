from pymongo import MongoClient, DESCENDING
from datetime import timezone

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

def insert(**kwargs):
    if kwargs:
        requests_collection = connect()
        requests_collection.insert_one(kwargs)
    else:
        print('nenhum dado foi informado')


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