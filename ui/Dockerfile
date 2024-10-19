# ---- Base Node ----
FROM node:20.18.0-alpine AS dependencies
LABEL org.opencontainers.image.source="https://github.com/PromptSail/prompt_sail"
WORKDIR /app
COPY package*.json ./

# ---- Dependencies ----
#FROM base AS dependencies
#RUN apk --no-cache add curl
RUN npm ci && npm cache clean --force

# ---- Copy Files/Build ----
FROM dependencies AS build

ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV


COPY . ./
RUN npm run build --omit=dev


# Stage 2, use the compiled app, ready for production with Nginx
FROM nginx:1.25-alpine-slim


COPY --from=build /app/dist /usr/share/nginx/html

# copy the custom nginx configuration
COPY /deployment/nginx-custom.conf /etc/nginx/conf.d/default.conf
# copy the custom entrypoint script that replaces the placeholders in the ui/.env.production file
COPY /deployment/docker_env_replacement.sh /docker-entrypoint.d/docker_env_replacement.sh

RUN chmod +x /docker-entrypoint.d/docker_env_replacement.sh

# Set proper permissions and switch to non-root user
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1

CMD ["nginx", "-g", "daemon off;"]
