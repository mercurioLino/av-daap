from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []



class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # the session should begin with a session_started event
        events = [SessionStarted()]

        # any slots that should be carried over should come after the
        # session_started event
        #events.extend(self.fetch_slots(tracker))

        # an action_listen should be added at the end as a user message follows
        dispatcher.utter_message(response="utter_greet")
        events.append(ActionExecuted("action_listen"))


        return events





# --------------- Actions que setam os valores dos Slots booleanos -----------------------------
# slot animal_urgency
class ActionSetAnimalUrgency(Action):
    def name(self):
        return "action_set_animal_urgency"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation" or intent == "wanna_animal_urgency":
            print('affirmation')
            return [SlotSet("animal_urgency", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("animal_urgency", False)]
        return []



# slot medical_attention
class ActionSetAnimalMedicalAttention(Action):
    def name(self):
        return "action_set_medical_attention"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation":
            print('affirmation')
            return [SlotSet("medical_attention", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("medical_attention", False)]
        return []


# slot private_property
class ActionSetPrivateProperty(Action):
    def name(self):
        return "action_set_private_property"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation":
            print('affirmation')
            return [SlotSet("private_property", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("private_property", False)]
        return []

# slot maus_tratos
class ActionSetTratos(Action):
    def name(self):
        return "action_set_maus_tratos"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation":
            print('affirmation')
            return [SlotSet("maus_tratos", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("maus_tratos", False)]
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
