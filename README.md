# SCAIP Gateway

A simple HTTP to SCAIP over SIP gateway.


1. run `docker-compose up` to start the service
2. open http://0.0.0.0:8000/docs
3. `docker-compose restart` to restart the service (unfortunately to [auto-reload](https://fastapi.tiangolo.com/#run-it) does not work due to the SIP-Thread)