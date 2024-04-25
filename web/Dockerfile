FROM node:18.18-alpine

WORKDIR /web

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build

ARG AI_SERVICE_PORT=8081
ARG AI_SERVICE_HOST=ai_service

ENV AI_API_PORT=$AI_SERVICE_PORT
ENV AI_API_HOST=$AI_SERVICE_HOST

ENV NODE_ENV=production

EXPOSE 8080

ENTRYPOINT [ "npm", "run", "start" ]