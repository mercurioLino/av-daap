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
Action que define o valor dos slots de endereço.
'''
class ActionSetActivictyDetailsPreference(Action):
    def name(self):
        return "action_set_address_details_preference"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirm" or intent == "define_address_detail":
            print('affirm')
            return [SlotSet("address_landmark", None)]
        elif intent == "deny":
            print('deny')
            return [SlotSet("address_number", -1), SlotSet("address_street", 'Desconhecido'), SlotSet("address_district", 'Desconhecido'), SlotSet("address_number", 'Desconhecido')]
        return []
