# ---- Base Node ----
FROM node:20-alpine AS base
LABEL org.opencontainers.image.source="https://github.com/PromptSail/prompt_sail"
WORKDIR /app
COPY package*.json ./

# ---- Dependencies ----
FROM base AS dependencies
RUN apk --no-cache add curl
RUN npm ci && npm cache clean --force

# ---- Copy Files/Build ----
FROM dependencies AS build

ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV


COPY . ./
RUN npm run build --omit=dev


# Stage 2, use the compiled app, ready for production with Nginx
FROM nginx:1.21.6-alpine


COPY --from=build /app/dist /usr/share/nginx/html

# copy the custom nginx configuration
COPY /deployment/nginx-custom.conf /etc/nginx/conf.d/default.conf
# copy the custom entrypoint script that replaces the placeholders in the ui/.env.production file
COPY /deployment/docker_env_replacement.sh /docker-entrypoint.d/docker_env_replacement.sh

RUN chmod +x /docker-entrypoint.d/docker_env_replacement.sh


