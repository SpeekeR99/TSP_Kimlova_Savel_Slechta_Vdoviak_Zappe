FROM python:3.9-slim

ENV ENV=production

WORKDIR /ai

# updates archive area
RUN echo "deb http://deb.debian.org/debian bookworm contrib non-free" > /etc/apt/sources.list.d/contrib.list
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 ttf-mscorefonts-installer fontconfig

# refresh system font cache
RUN fc-cache -f -v

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG MONGO_SERVICE_PORT=27017
ARG MONGO_SERVICE_HOST=mongodb_service

ENV MONGO_DB_PORT=$MONGO_SERVICE_PORT
ENV MONGO_DB_HOST=$MONGO_SERVICE_HOST

EXPOSE 8081

CMD ["python", "src/api/api_gateway.py"]