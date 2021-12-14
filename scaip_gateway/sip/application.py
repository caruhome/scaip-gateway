from sipsimple.application import SIPApplication
from sipsimple.storage import MemoryStorage
from application.notification import NotificationCenter
from sipsimple.core import FromHeader, Message, RouteHeader, SIPURI, ToHeader, Registration, Credentials, ContactHeader
from scaip_gateway.spec import ScaipRequest, ScaipResponse
from scaip_gateway.xml import Mrs, Mrq
from scaip_gateway.config import Configuration
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
import logging
import asyncio
from asyncio import Future
from weakref import WeakValueDictionary
from fastapi import HTTPException

logger = logging.getLogger()

class Application(SIPApplication):
    def __init__(self, *, config: Configuration) -> None:
        self.config = config

        self.serializer = XmlSerializer(config=SerializerConfig(pretty_print=False))
        self.parser = XmlParser(context=XmlContext())
        self.requests: WeakValueDictionary[str, Future] = WeakValueDictionary({})
        super().__init__()

    def start(self):
        notification_center = NotificationCenter()
        notification_center.add_observer(self, name='SIPEngineGotMessage')
        notification_center.add_observer(self, name='SIPMessageDidSucceed')
        notification_center.add_observer(self, name='SIPMessageDidFail')
        notification_center.add_observer(self, name='SIPApplicationDidStart')
        super().start(MemoryStorage())

    async def send_request(self, arc_name: str, scaip_request: ScaipRequest):
        logger.info(f"send_request to {arc_name}: {scaip_request}")

        config = self.config
        arc_config = config.get_arc_config(arc_name)

        if not arc_config:
            raise ValueError(f"no configuration found for ARC {arc_name}")

        xml_model = scaip_request.to_xml_model()
        xml_str = self.serializer.render(xml_model)

        result = self.new_result_future(scaip_request.reference)
        sender = self.get_sender()
        receiver = SIPURI(user=arc_config.username, host=arc_config.hostname, port=arc_config.port)
        message = Message(
            sender,
            ToHeader(receiver),
            RouteHeader(receiver),
            'application/scaip+xml',
            xml_str
        )
        message.send()
        logger.info(f"sent message: {xml_str}")

        scaip_response = await result

        logger.info(f"received response: {scaip_response}")

        return scaip_response

    def _NH_SIPApplicationDidStart(self, notification):
        logger.info("SIPApplicationDidStart")

    def _NH_SIPMessageDidSucceed(self, notification):
        logger.info("SIPMessageDidSucceed")

    def _NH_SIPMessageDidFail(self, notification):
        logger.info("SIPMessageDidFail")

        message = notification.sender
        xml_model = self.parser.from_bytes(message.body, Mrq)

        result = self.requests.get(xml_model.ref, None)

        if result:
            # TODO: return proper error
            result.set_exception(HTTPException(status_code=500, detail="SIPMessageDidFail"))

    def _NH_SIPEngineGotMessage(self, notification):
        logger.info("SIPEngineGotMessage")
        logger.info(f"got XML: {notification.data.body}")
        xml_model = self.parser.from_bytes(notification.data.body, Mrs)
        scaip_response = ScaipResponse.from_xml_model(xml_model)

        result = self.requests.get(xml_model.ref, None)

        if result:
            result.set_result(scaip_response)

    def get_sender(self):
        return FromHeader(self.get_source_uri())

    def new_result_future(self, reference: str) -> Future:
        loop = asyncio.get_running_loop()
        result = loop.create_future()
        self.requests[reference] = result
        return result

    def get_source_uri(self) -> SIPURI:
        sip_config = self.config.sip
        return SIPURI(user=sip_config.username, host=sip_config.hostname, port=sip_config.port)

