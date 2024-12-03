FROM node:20.17.0

WORKDIR /usr/src/back

COPY package.json ./

RUN npm install

COPY ./ ./

CMD [ "npx", "nodemon", "src/server.js" ]