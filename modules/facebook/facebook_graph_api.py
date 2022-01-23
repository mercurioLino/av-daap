from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
import requests

# pip install python-sdk
# pip install facebook-sdk


import facebook as fb
import json
from .download_images import dowload_face_images
'''
Busca o nome do usuário no facebook de acordo com seu id
'''
def get_user_name(sender_id):
    try:
        access_token = 'EAAJuk0ZAYiKwBANJuJwSIueONZCf8CDNmNtrvEy8BXM34Dmu9C20hXUP4atpv8ZALS0KaR5BBNrZAQWduQereuZAOWCj5XPNYEWRHEtZC24vrBeH5zEvb5V1Y11ZBHTfiRODI1ycgJosQdNQhXpqEhrJwr80awksN7YVXx70aQp4QDucAInTLnFVKhfHJbfU2EZD'
        r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name&access_token={}'.format(str(sender_id), access_token))

        # lança exeção se a resposta for 400
        # ou seja, quando o id estiver incorreto
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return ''
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        return ''
    
    # se chegou aqui a request deve ser 200
    # parsing dos valores
    response = r.json()
    if response:
        # verificar se o response não é none
        return response['first_name'] + ' ' + response['last_name']
    return ''
    

# realiza um post na página
# https://stackoverflow.com/questions/46805634/facebook-api-access-token-session-has-expired
def facebook_post(data, objectid):
    # token de acesso da página
    acess_token = 'EAAJuk0ZAYiKwBAAD720cb9KJuq07RCF1ZAyKf8ZByXk0dP0W2KyBjRILucSBRhMA8hmXWfBEkQLnVRE9B5UYB33EraXEZBgZAiqSAWkZCLnPMbJPt6JdTOTUJqMcO8hEdeB0QbAOFR071ITtxbOpQhB5twP6ClfwBCYdbW6qoKUEJLVV3DyyuX7lqmiULqVdVXYrojKKSzTWIZAZCjCitYfH'

    # instânciando objeto de acesso a API
    asafb = fb.GraphAPI(acess_token)
    

    # cria a messangem para o post
    message_data = make_rescue_post(data)

    if data['foto']:
        url = data['foto']
        # realiza o download das imagens informandas pela url
        res = dowload_face_images(url, objectid)

        # publicando multiplas imagens
        # https://github.com/mobolic/facebook-sdk/issues/401#issuecomment-354303521

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
        {data['animal_type']} com {data['animal_attributes']} precisa de ajuda.
        Saúde do animal: {data['animal_health']}
        Necessidade de urgência: {data['animal_urgency']}
        Necessidade de atendimento médico: {data['medical_attention']}
        Se encontra em propriedade privada: {data['private_property']}
        Esta sofrendo maus tratos {data['maus_tratos']}
        '''
    else:
        tipo = 'ANIMAL PARA ADOÇÃO'
        animal = f'''
        {data['animal_quantity']} {data['animal_type']}(s) para doação.
        Os animais são: {data['animal_attributes']}
        Vacinado? {data['is_vacinado']}
        Castrado? {data['is_castrado']}
        '''
    post = f'''
        {tipo}
        {animal}
        Endereço: {endereco}
        Referência: {data['address_landmark']}
    '''
    return post