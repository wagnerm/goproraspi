FROM container4armhf/armhf-alpine

RUN apk update && \
    apk add python py-pip py-pillow

RUN pip install argparse flake8 nose tox dateutils && \
    pip install goprohero

COPY main.py /main.py

ENV GOPROPW password
ENV INTV 60
ENV TTIME 60
ENV BEGIN ""

CMD python /main.py -p $GOPROPW -i $INTV -t $TTIME -b=$BEGIN
