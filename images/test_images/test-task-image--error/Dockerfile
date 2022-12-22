FROM python:3.8-buster

ENV PYTHONUNBUFFERED=0

RUN apt-get update
RUN apt-get install -y --force-yes postgresql-client
RUN apt-get install -y --force-yes curl

COPY requirements/requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY code /code
WORKDIR /code/

CMD ["bash", "/code/start_server.bash"]
