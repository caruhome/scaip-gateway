import os
import json

import boto3

from scaip_gateway.config import AlarmReceivingCenter, Configuration, SipConfiguration
from fastapi import FastAPI
from scaip_gateway.spec import ScaipRequest, ScaipResponse
from scaip_gateway.sip.application import Application
from dataclass_factory import Factory
from pathlib import Path
from urllib.parse import urlparse

factory = Factory()

config_path = os.environ.get("SCAIP_GATEWAY_CONFIG", None)
if not config_path:
    raise ValueError("Environment Variable SCAIP_GATEWAY_CONFIG missing")

config_path = urlparse(config_path, scheme="file", allow_fragments=False)

if config_path.scheme == "file":
    config_raw = json.loads(Path(config_path.path).read_text())
elif config_path.scheme == "ssm":
    client = boto3.client('ssm')
    config_raw = client.get_parameter(Name=config_path.path)
    config_raw = config_raw["Parameter"]["Value"]
    config_raw = json.loads(config_raw)

config = factory.load(config_raw, Configuration)

app = FastAPI()
sip = Application(config=config)
sip.start()

@app.post("/scaip/{arc_name}", response_model=ScaipResponse)
async def read_root(scaip_request: ScaipRequest, arc_name: str) -> ScaipResponse:
    return await sip.send_request(arc_name, scaip_request)

