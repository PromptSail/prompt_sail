# ---- Base Node ----
FROM node:20-alpine AS base
LABEL org.opencontainers.image.source="https://github.com/PromptSail/prompt_sail"
WORKDIR /app
COPY package*.json ./

# ---- Dependencies ----
FROM base AS dependencies
RUN apk --no-cache add curl
RUN npm ci

# ---- Copy Files/Build ----
FROM dependencies AS build

ARG NODE_ENV=production
ARG BACKEND_URL="http://promptsail-backend:8000"
ARG PROXY_URL_HOST="http://localhost:8000"
ARG SSO_GOOGLE_CLIENT_ID='******.apps.googleusercontent.com'
ARG SSO_AZURE_CLIENT_ID='6fe*******'
ARG SSO_AZURE_TENANT='4a1******'
ARG SSO_AZURE_SCOPES='user.read'
ARG SSO_AZURE_AUTHORITY='https://login.microsoftonline.com/4a1*****'

ENV NODE_ENV $NODE_ENV
ENV BACKEND_URL $BACKEND_URL
ENV PROXY_URL_HOST $PROXY_URL_HOST
ENV SSO_GOOGLE_CLIENT_ID $SSO_GOOGLE_CLIENT_ID
ENV SSO_AZURE_CLIENT_ID $SSO_AZURE_CLIENT_ID
ENV SSO_AZURE_TENANT $SSO_AZURE_TENANT
ENV SSO_AZURE_SCOPES $SSO_AZURE_SCOPES
ENV SSO_AZURE_AUTHORITY $SSO_AZURE_AUTHORITY

COPY . ./
RUN npm run build --omit=dev

# --- Release with Alpine ----
FROM node:20-alpine AS release
WORKDIR /app

COPY --from=build /app/package*.json ./
COPY --from=build /app/postcss.config.js ./
COPY --from=build /app/tailwind.config.js ./
COPY --from=build /app/tsconfig*.json ./
COPY --from=build /app/vite.config.ts ./

COPY --from=build /app/.env.production ./
COPY --from=build /app/dist ./dist
COPY --from=dependencies /app/node_modules ./node_modules

RUN ls -la /app/  # Debugging line
EXPOSE 5173
CMD [ "npm","run","preview" ]

# # Old build process
# FROM node:20-alpine
# LABEL org.opencontainers.image.source="https://github.com/PromptSail/prompt_sail"

# WORKDIR /app

# RUN apk --no-cache add curl

# COPY . ./

# RUN npm install

# COPY . ./

# RUN npm run build

# EXPOSE 5173

# CMD [ "npm","run","preview" ]