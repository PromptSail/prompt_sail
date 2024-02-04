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


#FROM node:20.11-bullseye-slim as node-base

# RUN apk --no-cache add curl

# ENV NODE_ENV production

# WORKDIR /app

# COPY . ./

# #RUN npm install
# RUN npm ci --only=production

# COPY . ./

# RUN npm run build

# EXPOSE 5173

# CMD [ "npm","run","preview" ]
