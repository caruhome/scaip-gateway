FROM python:3.7-stretch
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libssl-dev \
    libgmp3-dev \
    libmpfr-dev \
    libmpc-dev \
    libswscale-dev \
    libvpx-dev \
    libasound2-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavformat-dev \
    libavresample-dev \
    libavutil-dev \
    libpostproc-dev \
    libswresample-dev \
    libswscale-dev \
    libpjproject-dev
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /scaip-gateway

COPY . .
RUN poetry install

CMD [ "/bin/bash" ]