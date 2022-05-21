FROM python:3.9-alpine
LABEL maintainer='berkansems@gmail.com'

COPY ./requirements.txt /requirements.txt

COPY ./core /core
WORKDIR /core


RUN python -m venv /py && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"
CMD ["echo","Docker container build successfully"]
USER django-user