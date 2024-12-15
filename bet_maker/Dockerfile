FROM python:3.10.14

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app/

COPY ./src/start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 8000

ENTRYPOINT ["/start.sh"]

