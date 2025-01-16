FROM node:18.18-alpine

WORKDIR /web/doc/TSP

COPY package.json .

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

ENTRYPOINT [ "npm", "run", "serve" ]