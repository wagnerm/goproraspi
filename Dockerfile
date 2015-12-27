FROM container4armhf/armhf-alpine

RUN apk update && \
    apk add python py-pip py-pillow

RUN pip install argparse flake8 nose tox && \
    pip install goprohero

COPY main.py /root/main.py
