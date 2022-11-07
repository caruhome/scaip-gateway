from sipsimple.application import SIPApplication
from sipsimple.storage import MemoryStorage
from application.notification import NotificationCenter
from sipsimple.core import FromHeader, Message, RouteHeader, SIPURI, ToHeader, Registration, Credentials, ContactHeader, Engine, Route
from sipsimple.configuration import ConfigurationManager
from sipsimple.account import Account, AccountManager
from scaip_gateway.spec import ScaipRequest, ScaipResponse
from scaip_gateway.xml import Mrs, Mrq
from scaip_gateway.config import Configuration
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
import logging
import asyncio
import socket
from asyncio import Future
from weakref import WeakValueDictionary
from fastapi import HTTPException
from ursine import URI

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
        notification_center.add_observer(self, name='SIPEngineLog')
        notification_center.add_observer(self, name='SIPEngineSIPTrace')
        super().start(MemoryStorage())

    async def send_request(self, arc_name: str, scaip_request: ScaipRequest):
        logger.info(f"send_request to {arc_name}: {scaip_request}")

        config = self.config
        arc_config = config.get_arc_config(arc_name)
        arc_host = socket.gethostbyname(arc_config.hostname)

        if not arc_config:
            raise ValueError(f"no configuration found for ARC {arc_name}")

        xml_model = scaip_request.to_xml_model()
        xml_str = self.serializer.render(xml_model)
        result = self.new_result_future(scaip_request.reference)

        if arc_config.user:
            account = AccountManager().get_account(f"{arc_config.user.username}@{arc_host}")
            from_uri = account.uri
            credentials = account.credentials
        else:
            credentials = None
            if scaip_request.caller_id.startswith("sip") and scaip_request.caller_id not in ["sip:", "sips:"]:
                from_uri = SIPURI.parse(scaip_request.caller_id)
            else:
                from_uri = SIPURI(arc_host, user=scaip_request.controller_id)

        to_uri = SIPURI(host=arc_host, user=arc_config.username, port=arc_config.port)
        arc_route = Route(arc_host, port=arc_config.port, transport=arc_config.transport.value)

        logger.info(f"message.from_header: {message.from_header}")
        logger.info(f"message.to_header: {message.to_header}")
        logger.info(f"message.route_header: {message.route_header}")
        logger.info(f"message.credentials: {message.credentials}")
        message = Message(
            from_header=FromHeader(from_uri),
            to_header=ToHeader(to_uri),
            route_header=RouteHeader(arc_route.uri),
            content_type='application/scaip+xml',
            body=xml_str,
            credentials=credentials,
        )
        message.send(timeout=20)
        logger.info(f"sent message: {xml_str}")

        scaip_response = await result

        logger.info(f"received response: {scaip_response}")

        return scaip_response

    def new_result_future(self, reference: str) -> Future:
        loop = asyncio.get_running_loop()
        result = loop.create_future()
        self.requests[reference] = result
        return result

    def _NH_SIPApplicationDidStart(self, notification):
        logger.info("SIPApplicationDidStart")

        engine = Engine()
        engine.log_level = 5
        engine.trace_sip = True

        for arc_config in self.config.arcs:
            if arc_config.user:
                account = Account(f"{arc_config.user.username}@{arc_config.hostname}")
                logger.info(f"add Account for {arc_config.name} ({account.id})")
                account.display_name = arc_config.name
                account.enabled = True
                account.sip.register = False
                account.presence.enabled = False
                account.message_summary.enabled = False
                account.xcap.enabled = False
                account.auth.username = arc_config.user.username
                account.auth.password = arc_config.user.password
                account.save()

    def _NH_SIPMessageDidSucceed(self, notification):
        logger.info("SIPMessageDidSucceed")

    def _NH_SIPMessageDidFail(self, notification):
        reason = notification.data.reason
        if isinstance(reason, bytes):
            reason = reason.decode("utf-8")
        logger.error(
            f"SIPMessageDidFail: {reason} ({notification.data.code})",
        )
        if notification.data.code == 202:
            return

        message = notification.sender
        xml_model = self.parser.from_bytes(message.body, Mrq)
        result = self.requests.get(xml_model.ref, None)

        if result:
            result.set_exception(HTTPException(status_code=notification.data.code, detail=reason))

    def _NH_SIPEngineGotMessage(self, notification):
        logger.info("SIPEngineGotMessage")
        logger.info(f"got XML: {notification.data.body}")
        xml_model = self.parser.from_bytes(notification.data.body, Mrs)
        scaip_response = ScaipResponse.from_xml_model(xml_model)

        result = self.requests.get(xml_model.ref, None)

        if result:
            result.set_result(scaip_response)

    def _NH_SIPEngineLog(self, notification):
        logger.info(
            f"[{getattr(notification.data, 'sender', 'unknown')}]: {notification.data.message}"
        )

    def _NH_SIPEngineSIPTrace(self, notification):
        logger.info(f"SIPEngineSIPTrace: {notification.data.__dict__}")

