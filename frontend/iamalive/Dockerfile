FROM node:10.16.0-alpine as builder
COPY package.json package-lock.json ./
RUN npm ci && mkdir /iamalive && mv ./node_modules ./iamalive
COPY . ./iamalive

WORKDIR /iamalive

RUN npm run-script build_docker

WORKDIR /iamalive/dist/iamalive

FROM nginx:stable-alpine

COPY --from=builder /iamalive/dist/iamalive/ /usr/share/nginx/html

