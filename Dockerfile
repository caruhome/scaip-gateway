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

WORKDIR /scaip-gateway

COPY . .
RUN pip install --upgrade pip Cython
RUN pip install --editable .

CMD [ "bin", "bash" ]