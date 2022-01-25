from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
import requests
import re
import os

import facebook as fb
import json
from .download_images import dowload_face_images

# Busca o nome do usuário no facebook de acordo com seu id
def get_user_name(sender_id):
    try:
        access_token = os.environ['PAGE_ACESS_TOKEN']
        r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name&access_token={}'.format(str(sender_id), access_token))

        # lança exeção se a resposta for 400
        # ou seja, quando o id estiver incorreto
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return ''
    except requests.exceptions.RequestException as e:
        print(e)
        return ''
    
    # se chegou aqui a request deve ser 200
    # parsing dos valores
    response = r.json()
    if response:
        # verificar se o response não é none
        return response['first_name'] + ' ' + response['last_name']
    return ''
    

# realiza um post na página do Facebook
def facebook_post(data, objectid):
    # token de acesso da página
    acess_token = os.environ['PAGE_POST_ACESS_TOKEN']

    # instânciando objeto de acesso a API
    asafb = fb.GraphAPI(acess_token)
    
    # cria a messangem para o post
    message_data = make_rescue_post(data)

    if data['foto']:
        url = data['foto']
        # realiza o download das imagens informandas pela url
        res = dowload_face_images(url, objectid)

        photos = []
        for photo in res:
            try:
                # realiza o post da foto no facebook
                photo_posted = asafb.put_photo(image=photo, published=False)
                # utiliza o id do post para utilizar no post
                photos.append({'media_fbid': photo_posted['id']})
            except Exception as e:
                print(e)
                return
    
    # realiza o post ligando com as imagens postadas
    try:
        print('data', data)
        asafb.put_object("me", "feed", message=message_data, attached_media=json.dumps(photos))
    except Exception as e:
        print(e)
        return

# mapeia as respostas armazenadas pelo bot em algo legível para o receptor do email
def mapping_responses(original):
    if original is None:
        return 'Não Informado'
    elif original == -1:
        return 'Desconhecido'
    elif original == False:
        return 'Não'
    elif original == True:
        return 'Sim'
    else:
        return original


# Estrutura os dados para realizar a publicação
def make_rescue_post(data):
    tipo = ''
    animal = ''
    endereco = 'Desconhecido.'
    # Se o endereço detalhado é informado
    if data['address_district'] != 'Desconhecido':
        endereco = f"{data['address_street']} - {data['address_district']} Número {data['address_number']}"
    
    # apenas o rescue tem esse atributo
    if "private_property" in data:
        tipo = 'PEDIDO DE RESGATE'
        animal = f'''
        Animal: {data['animal_type']}.
        Características: {data['animal_attributes']}.
        Saúde do animal: {data['animal_health']}
        Necessidade de urgência: {mapping_responses(data['animal_urgency'])}
        Necessidade de atendimento médico: {mapping_responses(data['medical_attention'])}
        Se encontra em propriedade privada: {mapping_responses(data['private_property'])}
        Esta sofrendo maus tratos: {mapping_responses(data['maus_tratos'])}
        '''
    else:
        tipo = 'ANIMAL PARA ADOÇÃO'
        animal = f'''
        Animal: {data['animal_type']}.
        Quantidade: {data['animal_quantity']}.
        Características: {data['animal_attributes']}.
        Vacinado? {mapping_responses(data['is_vacinado'])}
        Castrado? {mapping_responses(data['is_castrado'])}
        '''
    post = f'''
        {tipo}
        ------------------------------------------------------
        {animal}
        ------------------------------------------------------
        Endereço: {endereco}
        Referência: {data['address_landmark']}
    '''
    post_formated = re.sub('^\s+', '', post, flags=re.MULTILINE)
    return post_formated