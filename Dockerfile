FROM ubuntu

MAINTAINER Martijn van Leeuwen (VOC) <info@voc-electronics.com>

LABEL Description="WiFiDomo Manager"

ENV DEBIAN_FRONTEND noninteractive

RUN echo "Updating system and installing python"

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y tar git curl wget dialog vim-addon-manager vim-syntax-docker vim-common build-essential
RUN apt-get install -y sed python python-dev python-distribute python-pip
RUN pip install flask

RUN mkdir -p /opt/WiFiDomo

COPY requirements.txt /opt/WiFiDomo/

RUN pip install -r /opt/WiFiDomo/requirements.txt

# Get pip to download and install requirements:
RUN pip install -r /my_application/requirements.txt

# Expose ports
EXPOSE 80 5000

# Set the default directory where CMD will execute
WORKDIR /opt/WiFiDomo/

# Set the default command to execute
# when creating a new container
CMD python run.py