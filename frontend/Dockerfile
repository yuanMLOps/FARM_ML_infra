# build production bundle
FROM node:24-alpine AS build

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
ARG VITE_API_URL
RUN npm run build

# serve the bundle with nginx
FROM nginx:1.27.0

COPY --from=build /app/dist /usr/share/nginx/html

