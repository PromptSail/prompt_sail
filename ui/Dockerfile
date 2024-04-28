# # ---- Base Node ----
# FROM node:20-alpine AS base
# LABEL org.opencontainers.image.source="https://github.com/PromptSail/prompt_sail"
# WORKDIR /app
# COPY package*.json ./

# # ---- Dependencies ----
# FROM base AS dependencies
# RUN apk --no-cache add curl
# RUN npm ci

# # ---- Copy Files/Build ----
# FROM dependencies AS build

# COPY . ./
# RUN npm run build

# # --- Release with Alpine ----
# FROM node:20-alpine AS release
# WORKDIR /app
# ARG NODE_ENV=production
# ENV NODE_ENV $NODE_ENV


# COPY --from=build /app/package*.json ./
# COPY --from=build /app/postcss.config.js ./
# COPY --from=build /app/tailwind.config.js ./
# COPY --from=build /app/tsconfig*.json ./
# COPY --from=build /app/vite.config.ts ./

# COPY --from=build /app/.env* ./
# COPY --from=build /app/dist ./dist
# COPY --from=dependencies /app/node_modules ./node_modules

# RUN ls -la /app/  # Debugging line
# EXPOSE 5173
# CMD [ "npm","run","preview" ]

# Old build process
FROM node:20-alpine
LABEL org.opencontainers.image.source="https://github.com/PromptSail/prompt_sail"

WORKDIR /app

RUN apk --no-cache add curl

COPY . ./

RUN npm install

COPY . ./

RUN npm run build

EXPOSE 5173

CMD [ "npm","run","preview" ]