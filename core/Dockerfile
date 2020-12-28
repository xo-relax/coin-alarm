# os : Debian 9 (stretch)
# python : 3.6.6
FROM python:3.6.6

LABEL maintainer="Xo Relax <m0.xo.relax@gmail.com>"

# install essential tools
RUN apt-get update && \
    apt-get install -y \
        apt-utils \
        apt-transport-https \
        debconf-utils \
        gcc \
        build-essential \
        poppler-utils


# install requirements & copy directories
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt