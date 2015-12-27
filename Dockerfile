FROM container4armhf/armhf-alpine

RUN apk update && \
    apk add python py-pip py-pillow

RUN pip install argparse flake8 nose tox && \
    pip install goprohero

COPY main.py /main.py

ENV GOPROPW password
ENV INTV 60
ENV TTIME 60

CMD python /main.py -p $GOPROPW -i $INTV -t $TTIME
