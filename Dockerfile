FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1

COPY . /src/
RUN pip install -r src/requirements.txt
WORKDIR /src/

EXPOSE 80