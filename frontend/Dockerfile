# frontend/Dockerfile
FROM node:20-alpine AS build

WORKDIR /app

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

COPY package*.json ./
RUN npm ci

COPY . .

RUN printf "VITE_API_BASE_URL=%s\n" "$VITE_API_BASE_URL" > .env.production

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
