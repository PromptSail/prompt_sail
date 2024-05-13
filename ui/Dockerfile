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


# Those are the environment variables that need to be set to placeholders in the ui/.env.production file
# at runtime the docker_env_replacement.sh script will replace the placeholders with the actual values from the environment variables

# ENV PORT=80
# ENV BACKEND_URL="PROMPT_SAIL_ENV_PLACEHOLDER_BACKEND_URLxxxxxx"
# ENV PROXY_URL_HOST="http://localhost:8000"
# ENV SSO_GOOGLE_CLIENT_ID='******.apps.googleusercontent.com'
# ENV SSO_AZURE_CLIENT_ID='6fe*******'
# ENV SSO_AZURE_TENANT='4a1******'
# ENV SSO_AZURE_SCOPES='user.read'
# ENV SSO_AZURE_AUTHORITY='https://login.microsoftonline.com/4a1*****'



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

#Old Dockerfile
# --- Release with Alpine ----
# FROM node:20-alpine AS release


# ENV PORT=80
# # ENV PROMPT_SAIL_ENV_PLACEHOLDER_BACKEND_URL='http://promptsail-backend:8000'
# # ENV PROMPT_SAIL_ENV_PLACEHOLDER_PROXY_URL_HOST='http://localhost:8000'
# ENV PROMPT_SAIL_ENV_PLACEHOLDER_SSO_GOOGLE_CLIENT_ID='change_me_docker.apps.googleusercontent.com'

# WORKDIR /app

# COPY --from=build /app/package*.json ./
# COPY --from=build /app/postcss.config.js ./
# COPY --from=build /app/tailwind.config.js ./
# COPY --from=build /app/tsconfig*.json ./
# COPY --from=build /app/vite.config.ts ./

# COPY --from=build /app/dist ./dist
# COPY --from=dependencies /app/node_modules ./node_modules


# COPY --from=build /app/deployment/docker_env_replacement.sh ./
# RUN chmod +x docker_env_replacement.sh
# RUN ./docker_env_replacement.sh

# # RUN ls -la /app/  # Debugging line
# # RUN ls -la /app/dist  # Debugging line
# # RUN ls -la /app/dist/assets  # Debugging line


# EXPOSE 80
# CMD [ "npm","run","preview" ]



