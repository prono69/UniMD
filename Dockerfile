# We're using Alpine stable
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Dependencies
RUN apk add --no-cache --update \
    git \
    dash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    build-base \
    python3 \
    redis \
    libxslt-dev \
    libxml2 \
    libxml2-dev \
    py-pip \
    libpq \
    build-base \
    linux-headers \
    jpeg-dev \
    curl \
    neofetch \
    sudo \
    gcc \
    python-dev \
    python3-dev \
    musl \
    sqlite \
    figlet \
    libwebp-dev \
    openssl \
    pv \
    jq \
    wget \
    bash

RUN pip3 install --upgrade pip setuptools

# Copy Python Requirements to /app
RUN  sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers
RUN adduser uniborg --disabled-password --home /home/uniborg
RUN adduser uniborg wheel
USER uniborg

#
# Install Python Packages
#
COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN sudo pip3 install -r requirements.txt

#
# Clone latest source - You might want to change this to your own repo
# If you want to use your local files, comment the git command and uncomment COPY
#
RUN mkdir /home/uniborg/uniborg
RUN git clone -b master https://github.com/baalajimaestro/Telegram-uniborg /home/uniborg/uniborg
#COPY . /home/uniborg/uniborg
RUN mkdir /home/uniborg/bin
WORKDIR /home/uniborg/uniborg

#
#Copies session and configs (if it exists)
#
COPY ./uniborg.session ./config.env* /home/uniborg/uniborg/
COPY ./client_secrets.json ./secret.json* /home/uniborg/uniborg/

#
# Finalization
#
RUN sudo chmod -R 777 /home/uniborg/uniborg
RUN curl -s https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o /home/uniborg/bin/megadown && sudo chmod a+x /home/uniborg/bin/megadown
RUN curl -s https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o /home/uniborg/bin/cmrudl && sudo chmod a+x /home/uniborg/bin/cmrudl
ENV PATH="/home/uniborg/bin:$PATH"
CMD ["dash","init/start.sh"]