FROM ubuntu:latest

RUN set -eux; \
    mkdir /app;

COPY ./main.py /app/
COPY ./img_gen /app/
COPY ./helpers.py /app/
COPY ./drinking_sentences.py /app/
COPY ./users.py /app/
COPY ./requirements.txt /app/

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
