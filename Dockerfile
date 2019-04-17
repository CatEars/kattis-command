# This is the dockerfile that is used by the testrunner

FROM ubuntu
RUN apt-get --quiet update -y && \
    apt-get --quiet upgrade -y && \
    apt-get --quiet install -y python3-dev python3-pip build-essential locales locales-all

RUN pip3 install virtualenv
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

WORKDIR /test
COPY bin bin
COPY kattcmd kattcmd
COPY test test
COPY setup.py setup.cfg requirements.txt pytest.ini Makefile ./

RUN rm -rf kattcmd/__pycache__ test/__pycache__

CMD make init && make install && make test
