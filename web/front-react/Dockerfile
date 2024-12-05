FROM node:20.17.0 as builder

WORKDIR /usr/src/front

COPY package.json ./

RUN npm install

COPY ./ ./

RUN npm run build

FROM nginx
EXPOSE 3000
COPY ./nginx-static/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /usr/src/front/build /usr/share/nginx/html