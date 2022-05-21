FROM python:3.9-alpine
LABEL maintainer='berkansems@gmail.com'

COPY ./requirements.txt /requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
ENV PYTHONUNBUFFERED 1
COPY ./core /core
WORKDIR /core

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install -r /requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"
CMD ["echo","Docker container build successfully"]
USER django-user