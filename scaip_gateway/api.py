import os
import json


from scaip_gateway.config import AlarmReceivingCenter, Configuration, SipConfiguration
from fastapi import FastAPI
from scaip_gateway.spec import ScaipRequest, ScaipResponse
from scaip_gateway.sip.application import Application
from dataclass_factory import Factory
from pathlib import Path

factory = Factory()

config_path = os.environ.get("SCAIP_GATEWAY_CONFIG", None)
if not config_path:
    raise ValueError("Environment Variable SCAIP_GATEWAY_CONFIG missing")
config_raw = json.loads(Path(config_path).read_text())
config = factory.load(config_raw, Configuration)

app = FastAPI()
sip = Application(config=config)
sip.start()

@app.post("/scaip/{arc_name}", response_model=ScaipResponse)
async def read_root(scaip_request: ScaipRequest, arc_name: str) -> ScaipResponse:
    return await sip.send_request(arc_name, scaip_request)

