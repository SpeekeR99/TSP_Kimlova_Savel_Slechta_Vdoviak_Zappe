FROM node:18.18-alpine

WORKDIR /web/doc/TSP

COPY package.json .

RUN npm install

RUN npm run build

COPY . .

EXPOSE 3000

ENTRYPOINT [ "npm", "run", "serve" ]