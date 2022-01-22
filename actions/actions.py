from typing import Any, Text, Dict, List


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, AllSlotsReset, Restarted

import requests

import os
print (os.getcwd())


from modules.facebook.facebook_graph_api import get_user_name
from modules.mail.email import send_rescue_email, send_donate_email
from modules.database.database import insert

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

        # sender_id = tracker.sender_id
        # print(sender_id)
        # user_name = get_user_name(sender_id)
        
        # setar uma mensagem personalizada se tiver nome
        # if user_name:
        #     pass

        # an action_listen should be added at the end as a user message follows
        # dispatcher.utter_message(response="utter_greet")
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

class ActionSetTermos(Action):
    def name(self):
        return "action_set_termos"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation":
            print('affirmation')
            return [SlotSet("termos", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("termos", False)]
        return []

class ActionSetIsCastrado(Action):
    def name(self):
        return "action_set_is_castrado"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation":
            print('affirmation')
            return [SlotSet("is_castrado", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("is_castrado", False)]
        return []

class ActionSetIsVacinado(Action):
    def name(self):
        return "action_set_is_vacinado"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation":
            print('affirmation')
            return [SlotSet("is_vacinado", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("is_vacinado", False)]
        return []

class ActionSetMoreHelp(Action):
    def name(self):
        return "action_set_more_help"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation":
            print('affirmation')
            return [SlotSet("more_help", True)]
        elif intent == "negation":
            print('negation')
            return [SlotSet("more_help", False)]
        return []

class ResetSlot(Action):   #Acrescentado por Biazom para uso no "Cancelamento/Retorno ao Menu Inicial"
  
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

class ActionRestarted(Action):   #Acrescentado por Biazom para uso no "Cancelamento/Retorno ao Menu Inicial"

    def name(self):
        return "action_chat_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]

'''
Action que define o valor dos slots de endereço.
'''
class ActionSetActivictyDetailsPreference(Action):
    def name(self):
        return "action_set_address_details_preference"

    def run(self, dispatcher, tracker, domain):

        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirmation" or intent == "define_address_detail":
            print('affirm')
            return [SlotSet("address_landmark", None)]
        elif intent == "negation":
            print('deny')
            return [SlotSet("address_number", -1), SlotSet("address_street", 'Desconhecido'), SlotSet("address_district", 'Desconhecido')]
        return []


# -------------------------- Fallback -------------------------------
# class ActionDefaultAskAffirmation(Action):
    
#     def name(self):
#         return "action_default_ask_affirmation"
        
#     def run(self, dispatcher, tracker, domain):
#         predicted_intent = tracker.latest_message["intent_ranking"][1]
#         print(predicted_intent)

#         intent_mappings = {
#             "rescue": "Resgate",
#             "affirmation": "que sim",
#             "negation": "que não",
#             "inform_animal_type": "Tipo do Animal",
#             "inform_animal_attributes": "as Características do Animal",
#             "donate": "Doação a DAAP",
#             "cancel": "teste"
#         }

#         message = "Sua intenção era informar " + intent_mappings[predicted_intent['name']] + "?"
            
#         message = "a"
#         print(predicted_intent['name'])
#         buttons = [
#             {"title": "Yes", "payload": "/{}".format(predicted_intent['name'])},
#             {"title": "No", "payload": "/out_of_scope"},         
#         ]
#         dispatcher.utter_message(message, buttons=buttons)
#         print('test')

#         return []


# --------------- Action que envia email -----------------------------
# class ActionEmailSender(Action):
#     def name(self):
#         return "action_email_sender"

#     def run(self, dispatcher, tracker, domain):
#         #Start do server
#         host = "smtp.gmail.com"
#         port = "587"
#         login = "epythonteste@gmail.com"
#         senha = "Compass123456"

#         server = smtplib.SMTP(host, port)
        
#         server.ehlo()
#         server.starttls()

#         server.login(login, senha)

#         #Construção do corpo do email
#         ##Texto com link
#         corpo = ''
#         email_msg = MIMEMultipart()
#         email_msg['From'] = login
#         email_msg['To'] = ''
#         email_msg['Subject'] = ""
#         email_msg.attach(MIMEText(corpo, 'html'))

#         ##Anexo
#         caminho_anexo = '' ##Inserir aqui o caminho do arquivo
#         attachment = open(caminho_anexo, 'rb')
#         att = MIMEBase('application', 'octet-stream')
#         att.set_payload(attachment.read())
#         encoders.encode_base64(att)
#         att.add_header('Content-Disposition', f'attachment; filename=') #Inserir no filename o nome do arquivo
#         attachment.close()
#         email_msg.attach(att)

#         #Envio do email
#         server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

#         #Fechando o servidor
#         server.quit()


class ActionGetAllSlotsData(Action):
    def name(self):
        return "action_all_slots_data"

    def run(self, dispatcher, tracker, domain):

        # Slots que são preenchidos nos dois casos
        # Slots do Contact
        age = tracker.get_slot('age')
        name = tracker.get_slot('name')
        phone = tracker.get_slot('phone')
        email = tracker.get_slot('email')
        # endereço
        address_details = tracker.get_slot('address_details')
        address_number = tracker.get_slot('address_number')
        address_street = tracker.get_slot('address_street')
        address_district = tracker.get_slot('address_district')
        address_landmark = tracker.get_slot('address_landmark')

        foto = tracker.get_slot('url')


        rescue_option = tracker.get_slot('rescue_option')

        
        # se o user escolheu o resgate
        if rescue_option and rescue_option == 'resgate':
            pass
            message = 'Solicitação de resgate'

            # rescue        
            animal_type = tracker.get_slot('animal_type')
            animal_attributes = tracker.get_slot('animal_attributes')
            animal_health = tracker.get_slot('animal_health')
            animal_urgency = tracker.get_slot('animal_urgency')
            medical_attention = tracker.get_slot('medical_attention')
            private_property = tracker.get_slot('private_property')
            maus_tratos = tracker.get_slot('maus_tratos')

            dados = f"""
                Dados do usuário
                Idade: {age}
                Nome: {name}
                Telefone: {phone}
                Email: {email}

                Dados do animal
                Tipo do Animal: {animal_type}
                Atributos: {animal_attributes}
                Saúde: {animal_health}
                Urgencia: {animal_urgency}
                Necessita de médico: {medical_attention}
                Está em propriedade privada: {private_property}
                Está em maus tratos: {maus_tratos}

                # Endereço
                Bairro: {address_district}
                Rua: {address_street}
                Número: {address_number}
                Referência: {address_landmark}
                Fotos: {foto}
            """
            print(dados)
            objectid, token = insert(age=age, name=name, phone=phone, email=email, animal_type=animal_type, animal_attributes=animal_attributes, animal_health=animal_health,
                    animal_urgency=animal_urgency, medical_attention=medical_attention, private_property=private_property, maus_tratos=maus_tratos,
                    address_district=address_district, address_street=address_street, address_number=address_number, address_landmark=address_landmark, foto=foto)

            send_rescue_email(age, name, phone, email, animal_type, animal_attributes, animal_health,
                    animal_urgency, medical_attention, private_property, maus_tratos,
                    address_district, address_street, address_number, address_landmark, foto, objectid, token)
            
        # se o user escolheu doação de animal
        else:
            #Slots para Give to Adoption
            animal_type = tracker.get_slot('animal_type')
            animal_attributes = tracker.get_slot('animal_attributes')
            animal_quantity = tracker.get_slot('animal_quantity')
            is_vacinado = tracker.get_slot('is_vacinado')
            is_castrado = tracker.get_slot('is_castrado')

            dados_doacao = f"""
                Dados do usuário
                Idade: {age}
                Nome: {name}
                Telefone: {phone}
                Email: {email}

                Dados do animal a ser adotado
                Tipo do Animal: {animal_type}
                Atributos: {animal_attributes}
                Quantidade: {animal_quantity}
                Vacinado: {is_vacinado}
                Castrado: {is_castrado}

                # Endereço
                Bairro: {address_district}
                Rua: {address_street}
                Número: {address_number}
                Referência: {address_landmark}
                Fotos: {foto}
            """
            print(dados_doacao)
            objectid, token = insert(age=age, name=name, phone=phone, email=email, animal_type=animal_type, animal_attributes=animal_attributes, animal_quantity=animal_quantity,
                    is_vacinado=is_vacinado, is_castrado=is_castrado, address_district=address_district, address_street=address_street, address_number=address_number, address_landmark=address_landmark, foto=foto)
            send_donate_email(age, name, phone, email, animal_type, animal_attributes, animal_quantity,
                    is_vacinado, is_castrado, address_district, address_street, address_number, address_landmark, foto, objectid, token)
            
        
        # #Outros Slots
        # url = tracker.get_slot('url')
        # termos = tracker.get_slot('termos')
        print('action final')
        return []


