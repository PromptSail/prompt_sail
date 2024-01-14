FROM node:20-alpine

WORKDIR /app

RUN apk --no-cache add curl

COPY . ./

RUN npm install

COPY . ./

RUN npm run build

EXPOSE 5173

CMD [ "npm","run","preview" ]
