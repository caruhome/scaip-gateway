FROM python:3.7-buster
RUN wget -O /etc/apt/trusted.gpg.d/agp-debian-key.gpg http://download.ag-projects.com/agp-debian-key.gpg
RUN echo 'deb http://ag-projects.com/debian buster main' >> /etc/apt/sources.list
RUN echo 'deb-src http://ag-projects.com/debian buster main' >> /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt-get update && apt-get install -y python3-sipsimple
ENV PYTHONPATH /usr/lib/python3/dist-packages/

WORKDIR /scaip-gateway

COPY . .
RUN pip install --upgrade pip Cython
RUN pip install --editable .

CMD [ "bin", "bash" ]