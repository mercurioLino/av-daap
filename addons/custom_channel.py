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

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            print(request.args)
            
            # observar se tem o token na request
            objectid = request.args['objectid']
            token = request.args['token']
            
            # procura o documento no banco de dados
            document = get_by_id(str(objectid[0]))
            print('documento', document)
            # se o token estiver correto faz o post
            if document['token'] == str(token[0]):
                facebook_post(document, str(objectid[0]))


            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def test(request: Request):
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

            # await on_new_message(
            #     UserMessage(
            #         text,
            #         collector,
            #         sender_id,
            #         input_channel=input_channel,
            #         metadata=metadata,
            #     )
            # )
            # return null
            return response.json(None)



        # async def receive(request: Request) -> HTTPResponse:
        #     print('a')
        #     sender_id = request.json.get("sender") # method to get sender_id 
        #     print(sender_id)
        #     text = request.json.get("text") # method to fetch text
        #     input_channel = self.name() # method to fetch input channel
        #     metadata = self.get_metadata(request) # method to get metadata

        #     collector = CollectingOutputChannel()
            
        #     # include exception handling

        #     # await on_new_message(
        #     #     UserMessage(
        #     #         text,
        #     #         collector,
        #     #         sender_id,
        #     #         input_channel=input_channel,
        #     #         metadata=metadata,
        #     #     )
        #     # )
        #     # return null
        #     return response.json(collector.messages)

        return custom_webhook