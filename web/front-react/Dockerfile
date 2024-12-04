FROM node:20.17.0 as builder

WORKDIR /usr/src/front

COPY package.json ./

RUN npm install

COPY ./ ./

RUN npm run build

FROM nginx
EXPOSE 80
COPY --from=builder /usr/src/front/build /usr/share/nginx/html