FROM python:3.8-slim

RUN apt-get update && apt-get install -y default-mysql-client

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]