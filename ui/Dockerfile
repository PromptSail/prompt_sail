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
COPY . ./
RUN npm run build

# --- Release with Alpine ----
FROM node:20-alpine AS release
WORKDIR /app
COPY --from=build /app/build ./build
COPY --from=dependencies /app/node_modules ./node_modules
EXPOSE 5173
CMD [ "npm","run","preview" ]

# Old build process
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