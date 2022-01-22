from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
import requests


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
        print(response['first_name'])
        print(response['last_name'])
        return response['first_name'] + ' ' + response['last_name']
    return ''
    


# pip install python-sdk

import facebook as fb
import json
from .download_images import dowload_face_images
# realiza um post na página
def facebook_post(data, objectid):
    # from lib import GraphAPI

    # token de acesso da página
    acess_token = 'EAAJuk0ZAYiKwBAFKXBIsCFTZC1jh5urZCUo45rDuTufDHfZBtFGa7pKC0J6MZBNwlsmrKZAZAQAzWR2zk2maXBwzrPR4END3kbRN3QJYz85ZATRTN5IBKZAuLGSKHziNvBJDA4jlITNE3kiPlBMLjpaZBsOdzOuCBGebmalzW1bNZCNt2ZAxyakQRdAmOZBgqe6a2O0hKglxoMMnYpoSc0ZAZAakTvt'

    # instânciando objeto de acesso a API
    asafb = fb.GraphAPI(acess_token)


    url = ['https://scontent.ftjl2-1.fna.fbcdn.net/v/t1.15752-9/253420484_422418932796081_2887210844616237437_n.jpg?_nc_cat=111&ccb=1-5&_nc_sid=ae9488&_nc_ohc=QFSJwjU5NB8AX8NFIuR&_nc_ht=scontent.ftjl2-1.fna&oh=03_AVIJRUzwekVUOYLfA0sSIQ_D83ykROCOegQOf-_nj_SpDQ&oe=6212DD1C']
    # realiza o download das imagens informandas pela url
    res = dowload_face_images(url, objectid)

    # publicando multiplas imagens
    # https://github.com/mobolic/facebook-sdk/issues/401#issuecomment-354303521

    photos = []
    for photo in res:
        # realiza o post da foto no facebook
        photo_posted = asafb.put_photo(image=photo, published=False)
        # utiliza o id do post para utilizar no post
        photos.append(
            {
                'media_fbid': photo_posted['id']
            }
        )
    # realiza o post ligando com as imagens postadas
    asafb.put_object("me", "feed", message=data, attached_media=json.dumps(photos))



    # ret = asafb.put_photo(image=open("test.jpeg", 'rb'),
                    # message=test)

    # publicando multiplas imagens
    # https://github.com/mobolic/facebook-sdk/issues/401#issuecomment-354303521
    # photo_id1 = asafb.put_photo(image=open('ny-1.jpg', 'rb'), published=False)
    # photo_id2 = asafb.put_photo(image=open('testando.jpeg', 'rb'), published=False)
    # asafb.put_object("me", "feed", message="Message with multiple files1!", attached_media=json.dumps([
                                                                                                    # {'media_fbid': str(photo_id1.get('id', ''))},
                                                                                                    # {'media_fbid': str(photo_id2.get('id', ''))}]))
