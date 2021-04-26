# SCAIP Gateway

A experimental HTTP to SCAIP over SIP gateway.
Not intended for production use!

## Configuration

1. create `config.json` (see [config.py](scaip_gateway/config.py) for structure)
2. create `.env` file with `SCAIP_GATEWAY_CONFIG` pointing to `config.json`


## Development

1. run `docker-compose up` to start the service
2. open http://0.0.0.0:8000/docs
3. `docker-compose restart` to restart the service (unfortunately to [auto-reload](https://fastapi.tiangolo.com/#run-it) does not work due to the SIP-Thread)