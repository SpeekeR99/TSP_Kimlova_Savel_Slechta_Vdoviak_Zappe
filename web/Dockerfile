FROM node:18.18-alpine
WORKDIR /web
COPY ./web/ /web/

RUN npm install
RUN npm run build

ENV NODE_ENV=production
EXPOSE 8080

ENTRYPOINT [ "npm", "run", "start" ]