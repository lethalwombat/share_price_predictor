# python base image
FROM python:3.8-slim-buster
USER root

# update runtime packages
RUN \ 
    apt-get update && \ 
    apt-get install -y

# copy requirements.txt into the container
COPY requirements.txt requirements.txt

# upgrade pip and setuptools
RUN \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

# copy applications assets into the container
COPY dash_app /dash_app
COPY helpers /helpers

# expose 8050 to the outside world
EXPOSE 8050
