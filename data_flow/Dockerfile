FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY ./enviroments/.env.docker /app/.env

WORKDIR /app/src

RUN mkdir -p /app/logs

RUN chmod -R 755 /app/logs

CMD ["python", "main.py"]
