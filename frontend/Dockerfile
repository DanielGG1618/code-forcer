FROM node:latest 

WORKDIR /app

COPY package.json .

RUN npm i --silent
RUN npm i -g serve --silent

COPY . /app/

RUN npm run build

CMD ["serve", "-s", "dist"]
