FROM ubuntu:latest

ENV Token=""

RUN set -eux; \
    mkdir /app;

COPY ./main.py /app/
COPY ./img_gen /app/
COPY ./drinking_sentences.py /app/
COPY ./requirements.txt /app/

RUN set -eux; \
    touch .env; \
    echo ${Token} | tee ./.env

RUN set -eux; \
    apt-get update; \
    apt-get install -y \
      pip \
      python3 \
      poppler-utils \
    ;

WORKDIR /app

RUN set -eux; \
    pip install -r ./requirements.txt;
    
CMD ["python3", "./main.py"]
