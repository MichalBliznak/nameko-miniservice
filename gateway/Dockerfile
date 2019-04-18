FROM python:3.6-slim

RUN apt-get update && apt-get -y install netcat curl && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh ./
COPY app.py ./
COPY auth.py ./
COPY errors.py ./
COPY settings.toml ./

RUN chmod +x ./run.sh

CMD ["./run.sh"]