FROM python:3.9 as builder

MAINTAINER caleb carvalho 

SHELL ["/bin/bash", "-c"]
ENV PYTHONUNBUFFERED 1
ENV BASEDIR /opt/python
ENV VENV ${BASEDIR}/venv
ENV APPDIR ${BASEDIR}/app
ENV LOG /var/log/web

RUN mkdir -p {$VENV,$APPDIR,$PEM_DIR,$LOG} 
COPY . ${APPDIR} 


WORKDIR ${APPDIR} 

RUN set -ex \
    && RUN_DEPS=" \
        supervisor \
        nginx \
    " \
    && BUILD_DEPS=" \
        build-essential \
        libpcre3-dev \
        libpq-dev \
        openssh-client \
        curl \
        git \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS $RUN_DEPS \
    && pip install -U pip virtualenv \
    && virtualenv ${VENV} \
    && source ${VENV}/bin/activate \
    && ${VENV}/bin/pip install poetry \
    && ${VENV}/bin/poetry install --without dev \
    && rm -rf /var/lib/apt/lists/*


EXPOSE 5000
CMD ${VENV}/bin/serve
#ENTRYPOINT ["/opt/python/app/.deploy/entrypoint.sh"]
