FROM python:3.9-slim

WORKDIR /ai

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ENV=production

EXPOSE 8080

CMD ["python", "src/api_gateway.py"]