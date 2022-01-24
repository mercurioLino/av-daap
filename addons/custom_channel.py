import asyncio
import inspect
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn

from modules.facebook.facebook_graph_api import facebook_post
from modules.database.database import get_by_id

import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from sqlalchemy import null

"""
Channel customizado criado apenas para que seja possível a realização de uma
publicação no Facebook atráves de um click no botão existente no email.

Esse channel fica escutando por requests e o botão, contido no corpo do email
enviado ao responsável pela página, realiza um request para o endpoint que realizará
a publicação no Facebook.

Esse Channel não envia nenhuma mensagem ao rasa diretamente. Todas as mensagem enviadas
ao rasa são de responsábilidade do outro Facebook Channel, esse apenas faz consultas ao
banco de dados e utiliza a API do Facebook para criação de posts na página da beneficiária.
"""
class MyIO(InputChannel):
    def name(name) -> Text:
        """Name of your custom channel."""
        return "myio"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:

        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )
        
        """
        Endpoint que recebe os dados necessário para buscar um documento no banco
        de dados e repassar os dados desse documento para o módulo do Facebook, o qual
        estrutura os dados e realiza uma publicação na página da beneficiária.
        """
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            print(request.args)
            
            # obtem os parâmetros contidos na query
            objectid = request.args['objectid']
            token = request.args['token']
            
            # procura o documento no banco de dados
            document = get_by_id(str(objectid[0]))
            # se o token estiver correto faz a publicação na página
            if document['token'] == str(token[0]):
                facebook_post(document, str(objectid[0]))
                return response.json({"status": "publicação realizado"})

            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request):
            print('test')
            sender_id = request.json.get("sender") # method to get sender_id 
            print(sender_id)
            text = request.json.get("text") # method to fetch text
            input_channel = self.name() # method to fetch input channel
            metadata = self.get_metadata(request) # method to get metadata

            collector = CollectingOutputChannel()
            print(collector)
            print(collector.messages)
            # include exception handling
           
            return response.json(None)

        return custom_webhook