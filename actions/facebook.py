from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
import requests


# Action que busca o nome do usuário que enviou a mensagem
class ActionGetUserName(Action):

    def name(self) -> Text:
        return "action_get_face_user_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        print(tracker.current_state()['sender_id'])
        sender_id = tracker.sender_id
        access_token = 'EAAJuk0ZAYiKwBANJuJwSIueONZCf8CDNmNtrvEy8BXM34Dmu9C20hXUP4atpv8ZALS0KaR5BBNrZAQWduQereuZAOWCj5XPNYEWRHEtZC24vrBeH5zEvb5V1Y11ZBHTfiRODI1ycgJosQdNQhXpqEhrJwr80awksN7YVXx70aQp4QDucAInTLnFVKhfHJbfU2EZD'
        r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name&access_token={}'.format(str(sender_id), access_token)).json()
        print(r)
        print(r['first_name'])
        print(r['last_name'])
        return []


# pip install python-sdk

# import facebook as fb
# import json

# realiza um post na página
def facebook_post():
    # from lib import GraphAPI

    # token de acesso da página
    acess_token = 'EAAJuk0ZAYiKwBAFKXBIsCFTZC1jh5urZCUo45rDuTufDHfZBtFGa7pKC0J6MZBNwlsmrKZAZAQAzWR2zk2maXBwzrPR4END3kbRN3QJYz85ZATRTN5IBKZAuLGSKHziNvBJDA4jlITNE3kiPlBMLjpaZBsOdzOuCBGebmalzW1bNZCNt2ZAxyakQRdAmOZBgqe6a2O0hKglxoMMnYpoSc0ZAZAakTvt'

    # instânciando objeto de acesso a API
    # asafb = fb.GraphAPI(acess_token)

    # ret = asafb.put_photo(image=open("test.jpeg", 'rb'),
                    # message=test)

    # publicando multiplas imagens
    # https://github.com/mobolic/facebook-sdk/issues/401#issuecomment-354303521
    # photo_id1 = asafb.put_photo(image=open('ny-1.jpg', 'rb'), published=False)
    # photo_id2 = asafb.put_photo(image=open('testando.jpeg', 'rb'), published=False)
    # asafb.put_object("me", "feed", message="Message with multiple files1!", attached_media=json.dumps([
                                                                                                    # {'media_fbid': str(photo_id1.get('id', ''))},
                                                                                                    # {'media_fbid': str(photo_id2.get('id', ''))}]))
