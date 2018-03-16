# This is the dockerfile that is used by the testrunner

FROM ubuntu
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y python3-dev python3-pip build-essential locales locales-all
RUN pip3 install --upgrade pip && pip3 install virtualenv
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8