FROM python:3.10-alpine

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN mkdir -p /code
ADD . /code
WORKDIR /code

RUN apk update && apk add py3-pip py3-virtualenv build-base ffmpeg && pip3 install -r requirements.txt && rm -rf /root/.cache

CMD ["sh"]
