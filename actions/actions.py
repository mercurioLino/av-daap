from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


'''
Action que define o valor do slot 'define_activicty_detail'.
Esse slot é o reponsável por expressar a vontade do usuário no quesito buscar atividade.
Uma atividade pode ser buscada de maneira aleatória ou não. No segundo caso o usuário
precisa informar alguns detalhes de sua atividade, somente nesse caso o form de atividades
será ativado, caso contrário, a requisição a API será realizada sem nenhum parâmetro.
'''
class ActionSetActivictyDetailsPreference(Action):
    def name(self):
        return "action_set_activicy_details_preference"

    def run(self, dispatcher, tracker, domain):
        # Define o valor do slot 'define_activicty_detail' como true ou false dependendo da
        # intenção do usuário. Se sua intenção para a pergunta de "definir detalhes da atividade"
        # for afirmativa, logo o valor será true. De maneira análoga, para intenção negativa o valor
        # será false. Esse valor é utilizado para realizar a requisião a BoredAPI.

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirm" or intent == "define_address_detail":
            print('affirm')
            return [SlotSet("address_details", True)]
        elif intent == "deny":
            print('deny')
            return [SlotSet("address_details", False)]
        return []

