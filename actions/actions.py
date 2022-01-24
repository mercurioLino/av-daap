from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, AllSlotsReset, Restarted

import os
print (os.getcwd())


from modules.facebook.facebook_graph_api import get_user_name
from modules.mail.send_mail import send_rescue_email, send_donate_email
from modules.database.database import insert
from modules.apis.nudity_detection_api import safe_api

"""
Customização da action que é executada quando o bot inicia.
Essa action, além de iniciar o bot, consulta a API do Facebook
para obter o nome do usuário que está estabelecendo a conversa com o bot.
Caso a conversa não esteja sendo realizada na plataforma do Facebook
o nome do usuário será obtido através de uma pergunta durante a conversa.
"""
class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # evento que inicia a sessão
        events = [SessionStarted()]

        # busca o nome do usuário através de seu id
        sender_id = tracker.sender_id
        user_name = get_user_name(sender_id)
        if (user_name != ''):
            events.append(SlotSet("name", user_name))

        events.append(ActionExecuted("action_listen"))
        return events


"""
Ao obter todas as infomações necessárias essa action é responsável por
repassar esses dados aos demais módulos do sistema.
Sendo eles: 
    módulo que envia email
    módulo que salva os dados no banco de dados
    módulo que analisa imagens e verifica possuem nudez, sangue ou contéudo agressivo
"""
class ActionGetAllSlotsData(Action):
    def name(self):
        return "action_all_slots_data"

    def run(self, dispatcher, tracker, domain):
        nudity_api = False

        # Slots que são preenchidos nos dois casos
        # Slots de informações do usuário
        age = tracker.get_slot('age')
        name = tracker.get_slot('name')
        phone = tracker.get_slot('phone')
        email = tracker.get_slot('email')
        
        # Slots de endereço
        address_details = tracker.get_slot('address_details')
        address_number = tracker.get_slot('address_number')
        address_street = tracker.get_slot('address_street')
        address_district = tracker.get_slot('address_district')
        address_landmark = tracker.get_slot('address_landmark')

        # imagens enviadas
        foto = tracker.get_slot('url')

        # slot que armazena se o user escolheu a opçao de resgate de animal
        rescue_option = tracker.get_slot('rescue_option')
        
        if rescue_option and rescue_option == 'resgate':
            # Slots referentes ao resgate do animal        
            animal_type = tracker.get_slot('animal_type')
            animal_attributes = tracker.get_slot('animal_attributes')
            animal_health = tracker.get_slot('animal_health')
            animal_urgency = tracker.get_slot('animal_urgency')
            medical_attention = tracker.get_slot('medical_attention')
            private_property = tracker.get_slot('private_property')
            maus_tratos = tracker.get_slot('maus_tratos')

            # insere os dados no banco
            objectid, token = insert(age=age, name=name, phone=phone, email=email, animal_type=animal_type, animal_attributes=animal_attributes, animal_health=animal_health,
                    animal_urgency=animal_urgency, medical_attention=medical_attention, private_property=private_property, maus_tratos=maus_tratos,
                    address_district=address_district, address_street=address_street, address_number=address_number, address_landmark=address_landmark, foto=foto)

            # passa a imagem pela api que busca nudez explicita
            safe = None
            if nudity_api is True:
                safe = safe_api(foto)

            # envia o email ao responsável pela página
            send_rescue_email(objectid=objectid, token=token, safe=safe, age=age, name=name, phone=phone, email=email, animal_type=animal_type, animal_attributes=animal_attributes, animal_health=animal_health,
                    animal_urgency=animal_urgency, medical_attention=medical_attention, private_property=private_property, maus_tratos=maus_tratos,
                    address_district=address_district, address_street=address_street, address_number=address_number, address_landmark=address_landmark, foto=foto)
            
        # se o user escolheu doação de animal
        else:
            # Slots referentes a adoção de animal
            animal_type = tracker.get_slot('animal_type')
            animal_attributes = tracker.get_slot('animal_attributes')
            animal_quantity = tracker.get_slot('animal_quantity')
            is_vacinado = tracker.get_slot('is_vacinado')
            is_castrado = tracker.get_slot('is_castrado')

            # insere os dados no banco
            objectid, token = insert(age=age, name=name, phone=phone, email=email, animal_type=animal_type, animal_attributes=animal_attributes, animal_quantity=animal_quantity,
                    is_vacinado=is_vacinado, is_castrado=is_castrado, address_district=address_district, address_street=address_street, address_number=address_number, address_landmark=address_landmark, foto=foto)
            
            # passa a imagem pela api que busca nudez explicita
            safe = None
            if nudity_api is True:
                safe = safe_api(foto)

            # envia o email ao responsável pela página
            send_donate_email(objectid=objectid, token=token, safe=safe, age=age, name=name, phone=phone, email=email, 
                    animal_type=animal_type, animal_attributes=animal_attributes, animal_quantity=animal_quantity,
                    is_vacinado=is_vacinado, is_castrado=is_castrado, address_district=address_district, 
                    address_street=address_street, address_number=address_number, address_landmark=address_landmark, foto=foto)
        
        dispatcher.utter_message(text="Tudo feito! Vou passar as informações para alguém que possa ajudar.")
        return []


# Acrescentado para uso no "Cancelamento/Retorno ao Menu Inicial"
class ResetSlot(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

# Acrescentado para uso no "Cancelamento/Retorno ao Menu Inicial"
class ActionRestarted(Action):
    def name(self):
        return "action_chat_restart"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_greet")
        return [Restarted()]


# --------------- Actions que setam os valores dos Slots booleanos -----------------------------
# slot animal_urgency
class ActionSetAnimalUrgency(Action):
    def name(self):
        return "action_set_animal_urgency"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("animal_urgency", True)]
        elif intent == "negation":
            return [SlotSet("animal_urgency", False)]
        return []

# slot medical_attention
class ActionSetAnimalMedicalAttention(Action):
    def name(self):
        return "action_set_medical_attention"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("medical_attention", True)]
        elif intent == "negation":
            return [SlotSet("medical_attention", False)]
        return []


# slot private_property
class ActionSetPrivateProperty(Action):
    def name(self):
        return "action_set_private_property"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("private_property", True)]
        elif intent == "negation":
            return [SlotSet("private_property", False)]
        return []

# slot maus_tratos
class ActionSetTratos(Action):
    def name(self):
        return "action_set_maus_tratos"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("maus_tratos", True)]
        elif intent == "negation":
            return [SlotSet("maus_tratos", False)]
        return []

# slot termos
class ActionSetTermos(Action):
    def name(self):
        return "action_set_termos"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("termos", True)]
        elif intent == "negation":
            return [SlotSet("termos", False)]
        return []

# slot is_castrado
class ActionSetIsCastrado(Action):
    def name(self):
        return "action_set_is_castrado"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("is_castrado", True)]
        elif intent == "negation":
            return [SlotSet("is_castrado", False)]
        return []

# slot is_vacinado
class ActionSetIsVacinado(Action):
    def name(self):
        return "action_set_is_vacinado"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("is_vacinado", True)]
        elif intent == "negation":
            return [SlotSet("is_vacinado", False)]
        return []

# slot more_help
class ActionSetMoreHelp(Action):
    def name(self):
        return "action_set_more_help"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation":
            return [SlotSet("more_help", True)]
        elif intent == "negation":
            return [SlotSet("more_help", False)]
        return []

# slots address_landmark
class ActionSetActivictyDetailsPreference(Action):
    def name(self):
        return "action_set_address_details_preference"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirmation" or intent == "define_address_detail":
            return [SlotSet("address_landmark", None)]
        elif intent == "negation":
            return [SlotSet("address_number", -1), SlotSet("address_street", 'Desconhecido'), SlotSet("address_district", 'Desconhecido')]
        return []