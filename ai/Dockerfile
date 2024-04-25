FROM python:3.9-slim

ENV ENV=production

WORKDIR /ai

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["python", "src/api/api_gateway.py"]