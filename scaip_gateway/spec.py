from scaip_gateway.xml import Mrq, Mrs
from pydantic import BaseModel, Field, stricturl
from datetime import datetime
from uuid import uuid4

from typing import Optional, Union
from enum import Enum

class SystemConfig(str, Enum):
    LOCAL_UNIT_AND_CONTROLLER = "0"
    GROUPED_EQUIPMENT_WITH_SUPERVISOR_OFF_DUTY = "1"
    GROUPED_EQUIPMENT_WITH_SUPERVISOR_ON_DUTY = "2"
    GROUPED_EQUIPMENT_WITH_SUPERVISOR_ON_DUTY_ACTING_AS_ALARM_RECEIVER = "3"

class CallHandling(str, Enum):
    OUTGOING_CALL = "0"
    CALLBACK = "1"

class MessageType(str, Enum):
    MESSAGE = "ME"
    RESET = "RE"
    INFORMATION = "IN"
    HEARTBEAT = "PI"

class HeartbeatOptions(str, Enum):
    UNADJUSTABLE = "0"
    ADJUSTABLE = "001"

class DeviceType(str, Enum):
    UNKNOWN = "0000"
    UNDEFINED = "0001"
    LOCAL_UNIT_AND_CONTROLLER = "0002"
    PERSONAL_TRIGGER = "0003"
    FIXED_TRIGGER = "0004"
    FALL_DETECTOR = "0005"
    PERSONAL_ATTACK_TRIGGER = "0006"
    PANIC_BUTTON = "0007"
    DUTY_SWITCH_REMOTE = "0008"
    DUTY_SWITCH_LOCAL = "0009"
    ACTIVITY_DETECTOR = "0010"
    PILL_DISPENSER = "0011"
    BED_MONITOR = "0012"
    MAT_SENSOR = "0013"
    DOOR_SENSOR = "0014"
    WANDERING_SENSOR = "0015"
    ENURESIS_DETECTOR = "0016"
    EPILEPSY_DETECTOR = "0017"
    OCCUPANCY_DETECTOR = "0018"
    HEART_RATE_MONITOR = "0019"
    ENVIRONMENTAL_MONITOR = "0020"
    GAS_DETECTOR = "0021"
    LIGHTING_CIRCUIT_MONITOR = "0022"
    SMOKE_DETECTOR = "0023"
    HEATING_SYSTEM_MONITOR = "0024"
    HEAT_DETECTOR = "0025"
    CARBON_MONOXIDE_DETECTOR = "0026"
    BOGUS_CALLER_SWITCH = "0027"
    INTRUDER_DETECTOR = "0028"
    BOUNDARY_DETECTOR = "0029"
    AUTOMATIC_MAN_DOWN_DETECTOR = "0030"
    SYSTEM_MONITOR = "0031"
    COMMUNICATION_LINK_MONITOR = "0032"
    FLOOD_DETECTOR = "0033"
    BATH_SENSOR = "0034"
    LATCH_KEY = "0035"
    PERIMETER = "0036"
    SPRINKLER = "0037"
    TAMPER = "0038"
    PRINTER = "0039"
    ROUTER = "0040"
    POWER_SUPPLY = "0041"
    ACCESS_CONTROLLER = "0043"
    CHAIR_MONITOR = "0044"
    CONTROLLER = "0045"
    ELEVATOR_ALARM_UNIT = "0046"
    FIRE_ALARM_SYSTEM = "0047"
    LOCAL_UNIT = "0048"
    MONITORING_DEVICE = "0049"
    RADIO_UNIT = "0050"
    TRACKING_DEVICE = "0051"

class DeviceComponent(str, Enum):
    UNKNOWN = "000"
    UNDEFINED = "001"
    BUTTON_1 = "002"
    BUTTON_2 = "003"
    BUTTON_3 = "004"
    BUTTON_4 = "005"
    BUTTON_5 = "006"
    SWITCH_1 = "007"
    SWITCH_2 = "008"
    SWITCH_3 = "009"
    SWITCH_4 = "010"
    SWITCH_5 = "011"
    OUTPUT_1 = "012"
    OUTPUT_2 = "013"
    OUTPUT_3 = "014"
    OUTPUT_4 = "015"
    OUTPUT_5 = "016"
    AUTOMATIC_CIRCUIT_1 = "017"
    AUTOMATIC_CIRCUIT_2 = "018"
    AUTOMATIC_CIRCUIT_3 = "019"
    AUTOMATIC_CIRCUIT_4 = "020"
    AUTOMATIC_CIRCUIT_5 = "021"
    ETHERNET_CIRCUIT = "022"
    MEMORY_CIRCUIT = "023"
    MICROCONTROLLER = "024"
    MODULE_1 = "025"
    MODULE_2 = "026"
    MODULE_3 = "027"
    MODULE_4 = "028"
    MODULE_5 = "029"

class StatusCode(str, Enum):
    UNKNOWN = "0000"
    UNDEFINED = "0001"
    ABORT = "0002"
    ABSENT = "0003"
    ACCEPTED = "0004"
    ACKNOWLEDGE = "0005"
    ACTIVATED = "0006"
    ACTIVE = "0007"
    ADDED = "0008"
    AUTOMATIC_ALARM = "0009"
    MANUAL_ALARM = "0010"
    ALERT = "0011"
    ARMED = "0012"
    ASSIGNED = "0013"
    BATTERY_FAILURE = "0014"
    BATTERY_OK = "0015"
    BATTERY_LOW = "0016"
    BUSY = "0017"
    BYPASS = "0018"
    CANCEL = "0019"
    CHARGED = "0020"
    CLOSED = "0021"
    CLOSED_TOO_LONG = "0022"
    IP_CONNECTION_FAILURE = "0023"
    IP_CONNECTION_REESTABLISHED = "0112"
    MOBILE_NETWORK_CONNECTION_FAILURE = "0024"
    MOBILE_NETWORK_CONNECTION_REESTABLISHED = "0113"
    POTS_CONNECTION_FAILURE = "0025"
    POTS_CONNECTION_REESTABLISHED= "0114"
    PRIMARY_COMMUNICATION_LINK_FAILURE = "0026"
    PRIMARY_COMMUNICATION_LINK_REESTABLISHED = "0115"
    REDUNDANT_COMMUNICATION_LINK_FAILURE = "0027"
    REDUNDANT_COMMUNICATION_LINK_REESTABLISHED = "0116"
    DELETED = "0028"
    DENIED = "0029"
    DISARMED = "0030"
    DISCONNECTED = "0031"
    ERROR_CODE_1 = "0032"
    ERROR_CODE_2 = "0033"
    ERROR_CODE_3 = "0034"
    ERROR_CODE_4 = "0035"
    ERROR_CODE_5 = "0036"
    ERROR_CODE_6 = "0037"
    ERROR_CODE_7 = "0038"
    ERROR_CODE_8 = "0039"
    ERROR_CODE_9 = "0040"
    EXECUTED = "0041"
    FAILURE = "0042"
    FREQUENCY_DRIFTED = "0043"
    FREQUENCY_DRIFTED_TO_LOWER_LEVEL = "0044"
    FREQUENCY_DRIFTED_TO_UPPER_LEVEL = "0045"
    HIGH_LEVEL = "0046"
    IN_PROGRESS = "0047"
    IN_SERVICE = "0048"
    INACTIVE = "0050"
    INITIATED = "0050"
    INTERRUPTED = "0051"
    JAMMED = "0052"
    LEVEL_1 = "0053"
    LEVEL_2 = "0054"
    LEVEL_3 = "0055"
    LEVEL_4 = "0056"
    LEVEL_5 = "0057"
    LEVEL_6 = "0058"
    LEVEL_7 = "0059"
    LEVEL_8 = "0060"
    LEVEL_9 = "0061"
    LOG = "0062"
    LOSS = "0063"
    LOW_LEVEL = "0064"
    MAINTENANCE_NEEDED = "0065"
    URGENT_MAINTENANCE_NEEDED = "0066"
    MALFUNCTION = "0067"
    MEMORY_FULL = "0068"
    NON_ACTIVE = "0069"
    NORMAL_STATE = "0070"
    OCCUPIED = "0071"
    OFF = "0072"
    OFFLINE = "0073"
    ON = "0074"
    ONLINE = "0075"
    OPEN = "0076"
    OPEN_TOO_LONG = "0077"
    OUT_OF_SERVICE = "0078"
    OVERFLOW = "0079"
    PENDING = "0080"
    PILL_NOT_TAKEN = "0081"
    PILL_REMINDER = "0082"
    PILL_TAKEN = "0083"
    PLANNED= "0084"
    POWER_FAILURE = "0085"
    POWER_RESTORED = "0086"
    PLANNED_PRESENCE = "0087"
    PRECENCE_AFTER_ALARM = "0088"
    PRIVACY_SWITCHED_OPERATED = "0089"
    PULSE = "0090"
    REESTABLISHED = "0091"
    AUTOMATIC_RESET = "0092"
    MANUAL_RESET = "0093"
    RESTORAL = "0094"
    RF_INTERFERENCE = "0095"
    STARTED = "0096"
    ENDED = "0097"
    SUBSTITUTED = "0098"
    SUCCEEDED = "0099"
    TEMPERATURE_HIGH = "0100"
    TEMPERATURE_LOW = "0101"
    TEST_TRANSMISSION_OVER_PRIMARY_CHANNEL = "0102"
    TEST_TRANSMISSION_OVER_REDUNDANT_CHANNEL = "0103"
    TIME_OUT = "0104"
    TROUBLE = "0105"
    TRESPASS = "0106"
    UNAUTHORIZED_ACCESS = "0107"
    UNBYPASS = "0108"
    VERIFIED = "0109"
    ASSISTANCE = "0110"
    INTERVENTION_COMPLETE = "0111"
    LYING_IN_BED = "0117"
    LOCKED = "0118"
    MOVEMENT = "0119"
    OCCUPANCY = "0120"
    PRESENT = "0121"
    RADIO_INTERFERENCE = "0122"
    RADIO_TEST_TRANSMISSION_MISSING = "0123"
    RADIO_TEST_TRANSMISSION_REESTABLISHED = "0124"
    TAMPER_ALARM = "0125"
    TEMPERATURE_RATE_OF_RISE = "0126"
    UNLOCKED = "0127"

class LocationCode(str, Enum):
    UNKNOWN = "000"
    UNDEFINED = "001"
    HOME = "002"
    AWAY = "003"
    INDOORS = "004"
    OUTDOORS = "005"
    INSIDE = "006"
    OUTSIDE = "007"
    AREA = "008"
    ZONE = "009"
    BASEMENT = "010"
    BATH_ROOM = "011"
    BED_ROOM = "012"
    DINING_ROOM = "013"
    FLOOR = "014"
    GARAGE = "015"
    GARDEN = "016"
    GARDEN_BACK = "017"
    GARDEN_FRONT = "018"
    GEO_FENCE = "019"
    GYM = "020"
    KITCHEN = "021"
    LAUNDRY = "022"
    RELAX = "023"
    SAUNA = "024"
    STAIRS = "025"
    STUDY_ROOM = "026"
    WORK_SHOP = "027"
    LOFT = "028"
    SHED = "029"
    TEMPORARY_ADDRESS = "030"
    SUMMER_HOUSE = "031"
    WINTER_COTTAGE = "032"
    MOBILE = "033"
    GEO_POSSITION_ATTACHED = "034"
    GPS_POSSITION_ATTACHED = "035"
    PROPERTY = "036"
    HANDICAP_BATH_ROOM = "037"
    DOOR = "038"
    FRONT_DOOR = "039"
    BACK_DOOR = "040"
    FIRE_DOOR = "041"
    HALWAY = "042"
    LIVING_ROOM = "043"
    APARTMENT = "044"
    BUNGALOW = "045"
    LOUNGE = "046"
    COMMUNAL_AREA = "047"
    OFFICE = "048"
    ROOM = "049"
    SITE = "050"
    WARD = "051"
    WING = "052"

class InfoCode(str, Enum):
    pass

def to_xml_model(api_model, xml_class):
    api_dict = api_model.dict(
        exclude_defaults=True,
        exclude_none=True,
        )
    xml_dict = {}
    for name, field in api_model.__fields__.items():
        scaip_key = field.field_info.extra["scaip"]
        
        api_value = getattr(api_model, name)
        if hasattr(api_value, 'to_xml_model'):
            api_value = api_value.to_xml_model()
        else:
            api_value = api_dict.get(name, None)

        if api_value:
            xml_dict[scaip_key] = api_value

    return xml_class(**xml_dict)

def from_xml_model(xml_model, api_class):
    api_dict = {}
    for name, field in api_class.__fields__.items():
        scaip_key = field.field_info.extra["scaip"]
        xml_value = getattr(xml_model, scaip_key)
        if xml_value:
            api_dict[name] = xml_value

    return api_class(**api_dict)

class LocationGeo(BaseModel):
    time_stamp: Optional[datetime] = Field(default=None, scaip='tim')
    wgs_pos: Optional[str] = Field(default=None, scaip='geo')
    gga_pos: Optional[str] = Field(default=None, scaip='gga')

    def to_xml_model(self) -> Mrq.Lge:
        return to_xml_model(self, Mrq.Lge)


class ScaipRequest(BaseModel):
    version: str = Field(const='01.00', default='01.00', scaip='ver')
    controller_id: str = Field(scaip='cid')
    device_type: Union[DeviceType, str] = Field(scaip='dty')
    system_config: SystemConfig = Field(default=SystemConfig.LOCAL_UNIT_AND_CONTROLLER, scaip='sco')
    call_handling: CallHandling = Field(default=CallHandling.OUTGOING_CALL, scaip='cha')
    message_type: MessageType = Field(default=MessageType.MESSAGE, scaip='mty')
    heartbeat_options: HeartbeatOptions = Field(default=HeartbeatOptions.UNADJUSTABLE, scaip='hbo')
    device_id: Optional[str] = Field(default=None, scaip='did')
    device_component: Optional[Union[DeviceComponent, str]] = Field(default=None, scaip='dco')
    device_text: Optional[str] = Field(default=None, scaip='dte')
    caller_id: str = Field(default="sip:", scaip='crd')
    status_code: Optional[Union[StatusCode, str]] = Field(default=None, scaip='stc')
    status_text: Optional[str] = Field(default=None, scaip='stt')
    priority: int = Field(ge=0, le=0, default=0, scaip='pri')
    location_code: Optional[Union[LocationCode, str]] = Field(default=None, scaip='lco')
    location_value: Optional[str] = Field(default=None, scaip='lva')
    # location_geo: Optional[LocationGeo] = Field(default=None, scaip='lge')
    location_text: Optional[str] = Field(default=None, scaip='lte')
    info_code: Optional[Union[InfoCode, str]] = Field(default=None, scaip='ico')
    info_text: Optional[str] = Field(default=None, scaip='ite')
    additional_message: Optional[int] = Field(default=None, scaip='ame')
    reference: str = Field(default_factory=lambda: uuid4().hex[:16], scaip='ref')

    def to_xml_model(self) -> Mrq:
        return to_xml_model(self, Mrq)

    @classmethod
    def from_xml_model(cls, xml_model):
        return from_xml_model(xml_model, cls)

class StatusNumber(str, Enum):
    OK = "0"
    MESSAGE_TOO_LONG = "1"
    INVALID_FORMAT = "2"
    WRONG_DATA_CONTENT = "3"
    HOLD = "4"
    NOT_TREATED = "5"
    BUSY = "6"
    MANDATORY_TAG_MISSING = "7"

class MediaReply(str, Enum):
    NO_VOICE_CALL = "0"
    DUPLEX_VOICE_CALL = "1"
    MICROPHONE_ONLY = "2"
    SPEAKER_ONLY = "3"

class CallhandlingReply(str, Enum):
    PRE_DEFINED_RECEIVER = "61"
    TRANSFERRED_NUMBER = "62"

class ScaipResponse(BaseModel):
    reference: str = Field(scaip='ref')
    status_number: Union[StatusNumber, int] = Field(scaip='snu')
    status_text: str = Field(default='', scaip='ste')
    common_version: Optional[str] = Field(default=None, scaip='cve')
    media_reply: MediaReply =  Field(default=MediaReply.NO_VOICE_CALL, scaip='mre')
    callhandling_reply: Union[CallhandlingReply, str] = Field(default=CallhandlingReply.PRE_DEFINED_RECEIVER, scaip='cre')
    transferred_number: Optional[str] = Field(default=None, scaip='tnu')
    heartbeat_interval: Optional[str] = Field(default=None, scaip='hbi')

    def to_xml_model(self) -> Mrs:
        return to_xml_model(self, Mrs)

    @classmethod
    def from_xml_model(cls, xml_model):
        return from_xml_model(xml_model, cls)

class DtmfCode(str, Enum):
    CLEAR_DOWN = "0"
    VOLUME_UP = "1"
    VOLUME_DOWN = "3"
    DUPLEX = "4"
    MICROPHONE_ONLY = "7"
    SPEAKER_ONLY = "8"
    OUTPUT_CONTROL = "9"